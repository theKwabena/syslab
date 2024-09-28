import docker
from docker import DockerClient
from fastapi import Depends
from deps.user import get_user_service
from typedef import UserServiceDep
from .user import UserService
from models.container import Container
from config.settings import settings
from core.deps import get_session

from docker.errors import APIError

from core.exceptions import EntityAlreadyExistsError, EntityDoesNotExistError, ServiceError
from sqlmodel import select, Session

from schemas.container import HostContainer


class DockerService:
    def __init__(self, session: Session):
        self.session = session
        self.user_service = UserService(session)
        try:
            self.client = DockerClient(settings.DOCKER_HOST_URL)
        except docker.errors.DockerException as e:
            raise ServiceError(f"Cannot connect to docker host {e}")
        except Exception as e:
            raise ServiceError(f"Cannot connect to docker host {e}")

    def test_client(self) -> bool:
        try:
            self.client.ping()
            return True
        except Exception as e:
            return False

    def container_exists(self, container_name: str) -> bool:
        container_name = f"username-{container_name}"
        try:
            self.client.containers.get(container_name)
            return True
        except docker.errors.NotFound:
            return False

    def list_host_containers(self):
        container_list = []
        try:
            containers = self.client.containers.list()
            for container in containers:
                container_list.append(
                    HostContainer(
                        id=container.id,
                        name=container.name,
                        status=container.status,
                        image=container.image.tags[0] if container.image.tags else 'unknown',
                    )
                )
            return container_list
        except docker.errors.NotFound:
            return None

    def list_user_containers(self) -> list[Container]:
        containers = self.session.exec(select(Container)).all()
        return containers

    def get_unused_port(self) -> (int, int):
        web_port = None
        dns_port = None
        used_ports = set()
        try:
            containers = self.client.containers.list()
            for container in containers:
                ports = container.attrs['NetworkSettings']['Ports']
                for port, mapping in ports.items():
                    if mapping:
                        used_ports.add(int(mapping[0]['HostPort']))

            for port in range(settings.DNS_PORT_START, settings.DNS_PORT_END):
                if port not in used_ports:
                    dns_port = port
                    break
            for port in range(settings.WEB_PORT_START, settings.WEB_PORT_END):
                if port not in used_ports:
                    web_port = port
                    break
        except Exception as e:
            raise ServiceError(f"Docker service unavailable {e}")
        return web_port, dns_port

    def get_last_container(self) -> Container | None:
        stmt = select(Container).order_by(Container.id.desc()).limit(1)
        return self.session.exec(stmt).first()

    def login_to_registry(self):
        result = False
        try:
            self.client.login(
                registry=settings.DOCKER_REPO_URL,
                username=settings.DOCKER_REPO_USER,
                password=settings.DOCKER_REPO_PASSWORD,
            )
            result = True
        except APIError as e:
            raise ServiceError(f"Cannot log in to remote repository {e}")
        return result

    def create_container(self, container_name: str) -> Container:
        if self.login_to_registry():
            if self.container_exists(container_name):
                raise EntityAlreadyExistsError(f"Container with name {container_name} already exist")
        try:
            web_port, dns_port = self.get_unused_port()
            ports = {
                "80": web_port,
                "53": dns_port
            }
            container = self.client.containers.run(
                tty=True,
                detach=True,
                ports=ports,
                stdin_open=True,
                name=f"username-{container_name}",
                image=settings.DEFAULT_UNIX_IMAGE,
                entrypoint="/bin/bash",
                restart_policy={"Name": "always"}
            )

            db_container = Container(
                web_port=web_port,
                dns_port=dns_port,
                container_id=container.id,
                container_name=container_name,
                host_name=settings.DOCKER_HOST_URL,
            )
            return db_container
        except docker.errors.APIError as de:
            raise ServiceError(f"Docker API service  failed {de}")
        except Exception as e:
            raise ServiceError(f"Docker service failed {e}")
            pass

    def get_user_environment(self, username) -> Container:
        user = self.user_service.get_user(username)
        if user is not None:
            if user.container is not None:
                if self.container_exists(user.container.container_name):
                    container = user.container
                else:
                    container = self.create_container(user.username)
                return container
            else:
                container: Container = self.create_container(user.username)
                user.container = container
                self.user_service.update_user(user)
                return user.container
        raise EntityDoesNotExistError(f"User with username {username} does not exist")

    # def get_user_container_id(self, username) -> str:
    #     client = self.get_host()
    #     if client is not None:
    #         print("Service")
    #         if DockerService.test_client(client):
    #             print("Next in line")
    #             lab_user = f"bootcamp-user-{username}"
    #             try:
    #                 # Check with db to get the host is stored on.
    #                 # check with the host if the container is running.
    #                 # If not start it and return the id to the frontend.
    #                 container_exists = client.containers.get(lab_user)
    #                 return container_exists.id
    #             except docker.errors.NotFound:
    #                 # container does not exist on the specific host. Start it.
    #                 container = client.containers.run(
    #                     tty=True,
    #                     detach=True,
    #                     name=lab_user,
    #                     stdin_open=True,
    #                     image="ubuntu:latest",
    #                     entrypoint="/bin/bash",
    #                 )
    #                 return container.id

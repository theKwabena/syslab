import docker
from docker import DockerClient
from fastapi import Depends
from deps.user import get_user_service
from typedef import UserServiceDep
from .user import UserService
from models.container import Container
from config.settings import settings
from core.deps import get_session
from sqlmodel import select, Session

from schemas.container import HostContainer


class DockerService:
    def __init__(self, session: Session):
        self.session = session
        self.user_service = UserService(session)
        try:
            self.client = DockerClient(settings.DOCKER_HOST_URL)
        except docker.errors.DockerException as e:
            print("Cannot connect to Host")
        except Exception as e:
            raise e

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

    def get_last_container(self) -> Container | None:
        stmt = select(Container).order_by(Container.id.desc()).limit(1)
        return self.session.exec(stmt).first()

    def create_container(self, container_name: str) -> Container:
        try:
            last_container = self.get_last_container()
            if last_container:
                last_used_dns_ports = last_container.dns_port
                last_used_web_ports = last_container.web_port
            else:
                last_used_dns_ports = 5500
                last_used_web_ports = 8000
            web_port = (last_used_web_ports + 1) if last_used_web_ports else 8000
            dns_port = (last_used_dns_ports + 1) if last_used_dns_ports else 5500
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
                image="ubuntu:latest",
                entrypoint="/bin/bash",
            )

            db_container = Container(
                web_port=web_port,
                dns_port=dns_port,
                container_id=container.id,
                container_name=container_name,
                host_name=settings.DOCKER_HOST_URL,
            )
            return db_container
        except Exception as e:
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
        raise Exception

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

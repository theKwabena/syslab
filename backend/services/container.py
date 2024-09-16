import docker
from docker import DockerClient
from fastapi import Depends
from deps.user import get_user_service
from typedef import UserServiceDep
from .user import UserService
from models.container import Container
from config.settings import settings


class DockerService:
    def __init__(self, user_service=Depends(get_user_service)):
        self.user_service = user_service
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
        try:
            self.client.containers.get(container_name)
            return True
        except docker.errors.NotFound:
            return False

    def create_container(self, container_name: str) -> str:
        try:
            container = self.client.containers.run(
                tty=True,
                detach=True,
                name=container_name,
                stdin_open=True,
                image="ubuntu:latest",
                entrypoint="/bin/bash",
            )
            return container.id
        except Exception as e:
            print(e)
            print("Host not found")

    def get_user_environment(self, username) -> Container:
        container = None
        user = self.user_service.get_user(username)
        if user is None:
            raise Exception  # TODO
        if user.container is not None:
            if self.container_exists(user.container.container_name):
                container = user.container
            else:
                self.create_container(user.username)
        else:
            new_container = self.create_container(user.username)
            container = Container(
                container_name=new_container,
            )
            user.container = container
            self.user_service.update_user(user)
        return container

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

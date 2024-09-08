import docker
from typing import List
from itertools import cycle
from docker import DockerClient


class DockerService:
    def __init__(self, hosts: List[str] = None):
        self.hosts = hosts
        self.hosts_cycle = cycle(self.hosts)

    @staticmethod
    def test_client(client: docker.DockerClient) -> bool:
        try:
            client.ping()
            return True
        except Exception as e:
            return False

    def get_host(self) -> DockerClient:
        client = None

        attempts = 0
        num_of_hosts = len(self.hosts)
        while attempts < num_of_hosts:
            try:
                client = DockerClient(base_url=next(self.hosts_cycle))
                break
            except docker.errors.DockerException as e:
                attempts += 1

        return client

    @staticmethod
    def container_exists(container_name: str, client: DockerClient) -> bool:
        try:
            client.containers.get(container_name)
            return True
        except docker.errors.NotFound:
            return False

    @staticmethod
    def create_container(container_name: str, client: docker.DockerClient) -> str:
        try:
            container = client.containers.run(
                tty=True,
                detach=True,
                name=container_name,
                stdin_open=True,
                image="ubuntu:latest",
                entrypoint="/bin/bash",
            )
            return container.id
        except Exception as e:
            pass

    def create_user_environment(self, username) -> str:
        client = self.get_host()
        if client is None:
            raise Exception("Docker client is not available")

        if DockerService.container_exists(username, client):
            raise Exception("Docker container already exists")
        else:
            container = DockerService.create_container(username, client)
            return container

    def get_user_container_id(self, username) -> str:
        client = self.get_host()
        if client is not None:
            print("Service")
            if DockerService.test_client(client):
                print("Next in line")
                lab_user = f"bootcamp-user-{username}"
                try:
                    # Check with db to get the host is stored on.
                    # check with the host if the container is running.
                    # If not start it and return the id to the frontend.
                    container_exists = client.containers.get(lab_user)
                    return container_exists.id
                except docker.errors.NotFound:
                    # container does not exist on the specific host. Start it.
                    container = client.containers.run(
                        tty=True,
                        detach=True,
                        name=lab_user,
                        stdin_open=True,
                        image="ubuntu:latest",
                        entrypoint="/bin/bash",
                    )
                    return container.id


serv = DockerService(["10.80.1.191:2375"])
print(serv.get_user_container_id("abbey"))
print(serv.get_user_container_id("abbey"))

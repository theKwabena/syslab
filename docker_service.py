import docker
from typing import List
from itertools import cycle
from docker import DockerClient


class DockerService:
    def __init__(self, hosts: List[str] = None):
        self.hosts = cycle(hosts)

    @staticmethod
    def test_client(client: docker.DockerClient) -> bool:
        try:
            client.ping()
            return True
        except Exception as e:
            return False

    def get_host(self) -> DockerClient:
        client = None
        try:
            client = DockerClient(base_url=next(self.hosts))
        except docker.errors.DockerException as e:
            pass
        return client

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

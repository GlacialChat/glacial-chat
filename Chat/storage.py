from django.conf import settings
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import File


from tempfile import NamedTemporaryFile
from os.path import join, basename


from dropbox import Dropbox
from dropbox.exceptions import ApiError


class DropBoxFile(File):
    def __init__(self, name, client):
        self.name = name
        self.client = client
        self._file = None

    @property
    def file(self):
        self._file = NamedTemporaryFile()
        self.client.files_download_to_file(self._file.name, self.name)
        self._file.flush()
        self._file.seek(0)
        return self._file


class DropBoxStorage(Storage):
    def __init__(self, oauth2_access_token=None, root_path=None):
        oauth2_access_token = oauth2_access_token or settings.DROPBOX_OAUTH2_TOKEN
        self.root_path = root_path or settings.DROPBOX_ROOT_PATH or '/'
        if oauth2_access_token is None:
            raise ImproperlyConfigured("You must configure a token auth of env var "
                                       "'DROPBOX_OAUTH2_TOKEN'.")
        self.client = Dropbox(oauth2_access_token)

    def delete(self, name):
        self.client.files_delete_v2(join(self.root_path, basename(name)))

    def exists(self, name):
        try:
            return bool(self.client.files_get_metadata(join(self.root_path, basename(name))))
        except ApiError:
            return False

    def url(self, name):
        media = self.client.files_get_temporary_link(join(self.root_path, basename(name)))
        return media.link

    def _open(self, name, mode='rb'):
        file = DropBoxFile(join(self.root_path, basename(name)), self.client)
        return file

    def _save(self, name, content: File):
        self.client.files_upload(content.read(), join(self.root_path, basename(name)))
        return name


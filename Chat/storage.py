"""
Contains DropBoxStorage as a storage location and DropBoxFile as a File handle
"""

from django.conf import settings
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import File
from django.utils.deconstruct import deconstructible

from tempfile import NamedTemporaryFile
from os.path import join, basename
from re import match

from dropbox import Dropbox
from dropbox.exceptions import ApiError


__all__ = ['DropBoxFile', 'DropBoxStorage']


class DropBoxFile(File):
    """
    A subclass of File that is designed specifically
    for use with DropBox, and used by DropBoxStorage
    """

    def __init__(self, _name: str, client: Dropbox):
        """
        :param _name: The full path of the location where the file is stored in DropBox
        :param client: The DropBox object in which is loaded with the OAUTH2 access token
        """
        self._name = _name
        self.client = client
        self._file = None

    @property
    def name(self):
        """
        Returns a formatted name of the file's name, using a regex match to remove
        unwanted parts of the name
        """
        mtc = match(r".*?([a-zA-Z0-9_-]+?)(_[a-zA-Z0-9]{7})?(\.[a-zA-Z0-9\._]+)?$", self._name)
        if mtc is None:
            return "Improperly_named.file"
        if mtc.group(3) is not None:
            return mtc.group(1) + mtc.group(3)
        return mtc.group(1)

    @property
    def file(self):
        """
        Returns a FileObject containing the content of the DropBoxFile, the
        FileObject is stored in a temp file, somewhere on disk
        """
        self._file = NamedTemporaryFile()
        self.client.files_download_to_file(self._file.name, self._name)
        self._file.flush()
        self._file.seek(0)
        return self._file


@deconstructible
class DropBoxStorage(Storage):
    """
    The default Storage base for all file storing of the Chat app
    """

    def __init__(self, oauth2_access_token: str = None, root_path: str = None):
        """
        The access token and root path may be provided here as well,
        if they are not provided here, program will check settings for environment variables

        :param oauth2_access_token: The OAUTH2 access token for the DropBox api
        :param root_path: The root path for storing the files in the DropBox storage, defaults '/'
        """
        oauth2_access_token = oauth2_access_token or settings.DROPBOX_OAUTH2_TOKEN
        self.root_path = root_path or settings.DROPBOX_ROOT_PATH or '/'
        if oauth2_access_token is None:
            raise ImproperlyConfigured("You must configure an OATH2 access token ENV named "
                                       "'DROPBOX_OAUTH2_TOKEN'.")
        self.client = Dropbox(oauth2_access_token)

    def delete(self, name: str):
        """
        Deletes the specified file from the storage system.
        """
        self.client.files_delete_v2(join(self.root_path, basename(name)))

    def exists(self, name: str):
        """
        Returns True if a file referenced by the given name already exists in the
        storage system, or False if the name is available for a new file.
        """
        try:
            return bool(self.client.files_get_metadata(join(self.root_path, basename(name))))
        except ApiError:
            return False

    def url(self, name: str):
        """
        Returns an absolute URL where the file's contents can be accessed
        directly by a Web browser.
        """
        media = self.client.files_get_temporary_link(join(self.root_path, basename(name)))
        return media.link

    def _open(self, name: str, mode: str = 'rb'):
        """
        Call DropBoxStorage.open(...) instead
        """
        file = DropBoxFile(join(self.root_path, basename(name)), self.client)
        return file

    def _save(self, name: str, content: File):
        """
        Call DropBoxStorage.save(...) instead
        """
        self.client.files_upload(content.read(), join(self.root_path, basename(name)))
        return name


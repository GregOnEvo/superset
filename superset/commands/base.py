# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from abc import ABC, abstractmethod
from typing import Any, List, Optional

from flask_appbuilder.security.sqla.models import User

from superset.commands.utils import populate_owners


class BaseCommand(ABC):
    """
        Base class for all Command like Superset Logic objects
    """

    @abstractmethod
    def run(self) -> Any:
        """
        Run executes the command. Can raise command exceptions
        :raises: CommandException
        """

    @abstractmethod
    def validate(self) -> None:
        """
        Validate is normally called by run to validate data.
        Will raise exception if validation fails
        :raises: CommandException
        """


class CreateMixin:
    @staticmethod
    def populate_owners(
        user: User, owner_ids: Optional[List[int]] = None
    ) -> List[User]:
        """
        Populate list of owners, defaulting to the current user if `owner_ids` is
        undefined or empty. If current user is missing in `owner_ids`, current user
        is added unless belonging to the Admin role.

        :param user: current user
        :param owner_ids: list of owners by id's
        :raises OwnersNotFoundValidationError: if at least one owner can't be resolved
        :returns: Final list of owners
        """
        return populate_owners(user, owner_ids, default_to_user=True)


class UpdateMixin:
    @staticmethod
    def populate_owners(
        user: User, owner_ids: Optional[List[int]] = None
    ) -> List[User]:
        """
        Populate list of owners. If current user is missing in `owner_ids`, current user
        is added unless belonging to the Admin role.

        :param user: current user
        :param owner_ids: list of owners by id's
        :raises OwnersNotFoundValidationError: if at least one owner can't be resolved
        :returns: Final list of owners
        """
        return populate_owners(user, owner_ids, default_to_user=False)

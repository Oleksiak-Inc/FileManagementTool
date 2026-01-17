from ..models import UserGroup
from ..extensions import db

class UserGroupService:

    @staticmethod
    def get_all_user_groups():
        return UserGroup.query.all()

    @staticmethod
    def get_user_group_by_id(user_group_id):
        return UserGroup.query.get(user_group_id)

    @staticmethod
    def get_user_group_by_name(name):
        return UserGroup.query.filter_by(name=name).first()

    @staticmethod
    def create_user_group(data):
        user_group = UserGroup(
            name=data.get('name'),
            created_by_id=data.get('created_by_id'),
            owner_id=data.get('owner_id')
        )
        db.session.add(user_group)
        db.session.commit()
        return user_group

    @staticmethod
    def update_user_group(user_group_id, data):
        user_group = UserGroup.query.get(user_group_id)
        if not user_group:
            return None
        
        if 'name' in data:
            user_group.name = data['name']
        if 'owner_id' in data:
            user_group.owner_id = data['owner_id']
        
        db.session.commit()
        return user_group

    @staticmethod
    def delete_user_group(user_group_id):
        user_group = UserGroup.query.get(user_group_id)
        if not user_group:
            return False
        
        db.session.delete(user_group)
        db.session.commit()
        return True

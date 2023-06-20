from app.crud.base import CRUDBase


class StudentsCRUD(CRUDBase):
    def __init__(self, collection):
        self.collection = collection
        super().__init__(collection)


class AssignmentsCRUD(CRUDBase):
    def __init__(self, collection):
        self.collection = collection
        super().__init__(collection)


class ProgressesCRUD(CRUDBase):
    def __init__(self, collection):
        self.collection = collection
        super().__init__(collection)


class StatusCRUD(CRUDBase):
    def __init__(self, collection):
        self.collection = collection
        super().__init__(collection)


students = StudentsCRUD('students')
assignments = AssignmentsCRUD('assignments')
progresses = ProgressesCRUD('progresses')
status = StatusCRUD('status')
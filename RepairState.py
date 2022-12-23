from abc import abstractmethod


class RepairState:
    @abstractmethod
    def switch_state(self, repair):
        """
        不同状态下的状态转移
        :param repair: 下一个转换的状态 Repair
        :return:
        """
        pass

    def get_id(self):
        pass


class TodoState(RepairState):
    """
    待调度状态
    """
    def __init__(self):
        super().__init__()

    def switch_state(self, repair):
        """
        被调度后，状态由TodoState转为DoingState
        :return:
        """
        repair.set_state(DoingState())

    def get_id(self):
        return 0


class DoingState(RepairState):
    """
    报修中状态
    """

    def __init__(self):
        super().__init__()

    def switch_state(self, repair):
        """
        当维修工人处理完故障后，状态转为DoneState
        :return:
        """
        repair.set_state(DoneState())

    def get_id(self):
        return 1


class DoneState(RepairState):
    """
    已报修状态
    """
    def __init__(self):
        super().__init__()

    def switch_state(self, repair):
        """
        已报修状态为终点状态，无需继续转换
        :return:None
        """
        pass

    def get_id(self):
        return 2
Complaint：投诉记录

Fault：故障

Feedback：评价记录

Manager：经理

Repair：报修

RepairState：报修状态基类

  - TodoState：待调度状态
  
  - DoingState：报修中状态
  
  - DoneState：报修完成状态
  
Schedule：调度

Scheduler：调度员

User：业主

Worker：维修工

WorkRecord：维修记录

main.py: 包含了测试的例子（报修、调度（多次调度）、维修记录、评价记录、投诉记录等）

------

**DONE**：基础流程和拓展流程代码已完全实现。

**TODO**：数据库的接入。目前是建立了一些字典来当作数据库，字典的key为id，字典的value为对应的值，可以参考字典的实现来完成数据库的接入。

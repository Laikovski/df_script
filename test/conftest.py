import pytest
from script import BaseExecutor, HumanRepresentationExecutor, InodeRepresentationExecutor
from subprocess import Popen, PIPE

def execute_script(params: str = ''):
    '''Run script with Parameters ex. "--human", "--inode"'''
    commands = ['python', '../script.py']
    if params:
        commands.append(params)
    process = Popen(commands, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr

@pytest.fixture(params=['--test', '--testing', '-false'])
def execute_param(request):
    '''Run script with invalid Parameters'''
    result = execute_script(request.param)
    return result

@pytest.fixture(scope='session')
def df_executor():
    '''fixture for executor class BaseExecutor'''
    return BaseExecutor()

@pytest.fixture(scope='session')
def human_executor():
    '''fixture for executor class HumanRepresentationExecutor'''
    return HumanRepresentationExecutor()

@pytest.fixture(scope='session')
def inode_executor():
    '''fixture for executor class HumanRepresentationExecutor'''
    return InodeRepresentationExecutor()


@pytest.fixture(scope='session')
def execute_run_df(df_executor):
    '''Fixture for Execute method run - df base'''
    return df_executor.run()

@pytest.fixture(scope='session')
def execute_run_hm(human_executor):
    '''Fixture for Execute method run - human representation'''
    return human_executor.run()

@pytest.fixture(scope='session')
def execute_run_inode(inode_executor):
    '''Fixture for Execute method run - inode representation'''
    return inode_executor.run()


@pytest.fixture()
def mock_df_executor(mocker):
    '''mocker with expected data for base representation'''
    def get_new_output(*args):
        return ["Filesystem     1K-blocks     Used Available Use% Mounted on",
                "udev            16352960        0  16352960   0% /dev"]

    mocker.patch('script.BaseExecutor.execute', get_new_output)
    return BaseExecutor()

@pytest.fixture()
def mock_human_executor(mocker):
    '''mocker with expected data for human representation'''
    def get_new_output(*args):
        return ["Filesystem      Size  Used Avail Use% Mounted on",
                "udev             16G     0   16G   0% /dev"]

    mocker.patch('script.HumanRepresentationExecutor.execute', get_new_output)
    return HumanRepresentationExecutor()

@pytest.fixture()
def mock_inode_executor(mocker):
    '''mocker with expected data for inode representation'''
    def get_new_output(*args):
        return ["Filesystem      Inodes  IUsed   IFree IUse% Mounted on",
                "udev           4088240    685 4087555    1% /dev"]

    mocker.patch('script.InodeRepresentationExecutor.execute', get_new_output)
    return InodeRepresentationExecutor()



import json
from conftest import execute_script
from subprocess import Popen, PIPE


class TestRepresentations:
    '''Set of tests for check valid output data'''

    def test_df_base_data(self, mock_df_executor, df_executor):
        ''' Get and compare data from mock output and df base output'''
        df_result = df_executor.main()
        mock_result = mock_df_executor.main()

        assert mock_result == df_result

    def test_human_data(self, mock_human_executor, human_executor):
        ''' Get and compare data from mock output and human representation output'''
        human_result = human_executor.main()
        mock_result = mock_human_executor.main()

        assert mock_result == human_result

    def test_inode_data(self, mock_inode_executor, inode_executor):
        ''' Get and compare data from mock output and inode representation output'''
        inode_result = inode_executor.main()
        mock_result = mock_inode_executor.main()

        assert mock_result == inode_result


class TestKeysOutput:
    '''Set test for compare output keya'''

    def test_keys_for_df(self, execute_run_df):
        '''get and compare keys for base df'''
        assert list(execute_run_df[0].keys()) == ['Filesystem', '1K-blocks', 'Used', 'Available', 'Use%', 'Mounted on']

    def test_keys_for_hm(self, execute_run_hm):
        '''get and compare keys for human representation'''
        assert list(execute_run_hm[0].keys()) == ['Filesystem', 'Size', 'Used', 'Avail', 'Use%', 'Mounted on']

    def test_keys_for_inode(self, execute_run_inode):
        '''get and compare keys for inode representation'''
        assert list(execute_run_inode[0].keys()) == ['Filesystem', 'Inodes', 'IUsed', 'IFree', 'IUse%', 'Mounted on']



def test_base_script(df_executor):
    '''Check stdout and stderr for base executor'''
    stdout, stderr = execute_script()
    assert not stderr, 'There are no errors during script execution'
    assert json.loads(stdout) == df_executor.main()

def test_human_script(human_executor):
    '''Check stdout and stderr for human executor'''
    stdout, stderr = execute_script('--human')
    assert not stderr, 'There are no errors during script execution'
    assert json.loads(stdout) == human_executor.main()

def test_inode_script(inode_executor):
    '''Check stdout and stderr for inode executor'''
    stdout, stderr = execute_script('--inode')
    assert not stderr, 'There are no errors during script execution'
    assert json.loads(stdout) == inode_executor.main()


def test_invalid_param(execute_param):
    '''run script with invalid parameters'''
    assert execute_param[1][1:40] == b'sage: script.py [-h] [--human] [--inode'
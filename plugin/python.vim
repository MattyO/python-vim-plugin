let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import sample

EOF

function! RunsSingleTest()
    python3 sample.run_command(sample.test_command('single'))
endfunction

function! RunAllTests()
    python3 sample.run_command(sample.test_command('all'))
endfunction

function! RunCommand(com)
    python3 sample.run_command(vim.eval('a:com'))
endfunction

command! -nargs=1 RunCommand call RunCommand()
command! -nargs=0 RunsSingleTest call RunsSingleTest()
command! -nargs=0 RunAllTests call RunAllTests()

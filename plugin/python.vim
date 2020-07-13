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

function! RunCoverage()
    python3 sample.run_command("coverage run --omit=env/*,tests/* -m unittest discover -v && coverage json")
endfunction

function! RunCommand(com)
    python3 sample.run_command(vim.eval('a:com'))
endfunction

function! CreateInits()
    python3 sample.create_inits()
endfunction

function! CreateTemplatedTestFile()
python3 << EOF
test_files_name, line_number = sample.create_templated_test_file()
vim.command("let s:testFileName = '%s'"% test_files_name )
vim.command("let s:testFileLineNumber= '%s'"% line_number )
EOF
	echo s:testFileName
	echo s:testFileLineNumber

	let s:windowNumber = win_findbuf(bufnr(s:testFileName))

	if len(s:windowNumber) == 0
		execute "vs ".s:testFileName
	else
		call win_gotoid(win_findbuf(bufnr(s:testFileName))[0])
		:edit!
		call cursor( s:testFileLineNumber, 0)
	:endif
endfunction


command! -nargs=1 RunCommand call RunCommand()
command! -nargs=0 RunsSingleTest call RunsSingleTest()
command! -nargs=0 RunAllTests call RunAllTests()
command! -nargs=0 RunCoverage call RunCoverage()
command! -nargs=0 CreateInits call CreateInits()
command! -nargs=0 CreateTemplatedTestFile call CreateInits()




python3 sample.create_sign()
au BufReadPost *.py python3 sample.create_signs_in_file(sample.get_sign_lines())

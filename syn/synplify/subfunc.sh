function replaceDotWithRoot(){
	dir_in=$1
	DIR_FLIST_ROOT=$2
	echo $DIR_FLIST_ROOT${dir_in./}
}

# case ./ and /some_dir
function casep_dir(){
	dir_in=$1
	DIR_FLIST_ROOT=$2
	first_char=${dir_in[0:]}
	#echo "===This is dir process..input is $1, first_char is:$first_char "

	case $first_char in
		"/")  echo $dir_in
		;;

		".")  echo $(replaceDotWithRoot ${dir_in} ${DIR_FLIST_ROOT} )
		;;

		"\$") echo $dir_in
		;;

		*) echo "ERROR: <casep_dir> undefined line head:"${first_char}
		;;
	esac
}

function travDirAndSub(){
	for file in $(ls $1)
	do
	    if [ -d $1"/"$file ]
	    then
		travDirAndSub $1"/"$file
	    else
		echo $1"/"$file    # ...
	    fi
	done
}

# case +incdir+
function casep_incdir(){
	DirInc=${1#+incdir+}
	DIR_WORK_ROOT=$2
	#echo $(casep_dir $DirInc  $DIR_WORK_ROOT)
}

function casep_v(){
	#arr_in=($1)     # change to arr
	# echo "Debug: input 2 is:$2, input 1 is:$1 "
	echo $2
}

#case +define+
function casep_define(){
	echo "=== This is +define+ process..."
	line_in=$1
	micro_def=${line_in#+define+}
	echo "\`define "$micro_def
}

#case .f process
function casep_dotf(){
	fn_dotF=$1
	DIR_FLIST_ROOT=$2
	fn_target=$3
	echo "=== This is .f process... fn_dotF is:"${fn_dotF}

	#cat this file and read
	cat $fn_dotF |sed "/^\$*$/d" | while read line   # cat the file, remove blank lines, loop read
	do
		first_char=${line:0:2}
		case $first_char in
			"//") echo "Info: // line. Will ignore this line:$line "
			;;

			"./" | "/"[a-z] | "/"[A-Z] | "\$"? )dir_line=$(casep_dir ${line}  ${DIR_FLIST_ROOT} )
				echo "add_file -verilog "${dir_line} >> ${fn_target}
			;;

			"+i") folderToAdd=$(casep_incdir ${line} $DIR_FLIST_ROOT)
				echo "set_option -include_path { ${fol;derToAdd} }" >> ${fn_target}
			;;

			"+d")  def_line=${casep_define ${line}}
				echo $def_line >> ${fn_target}
			;;

			"-f")  arr_line=($line)    # recurse
				fn_addr_relatv=${arr_line[1]}
				fn=$DIR_FLIST_ROOT${fn_addr_relatv#./}
				casep_dotf $fn $DIR_FLIST_ROOT ${fn_target}
			;;

			"-v")  v_line=(casep_v ${line})
				#vline=$(Vlines)$(echo $v_line)   # append
				echo "add_file -verilog -before ./define_compiler.svh ${v_line}" >> ${fn_target}
			;;

			#--- +libext+
			"+l" ) echo "Info: +libext+ line. Ignored."
			;;

			"\r" | " "  | "\n" | "\n\r") echo "Info: Blank line read:"${first_char}
			;;

			*) echo "ERROR: <casep_dotf> undefined line read:"${first_char}
			;;
		esac
	done   # end while read
}

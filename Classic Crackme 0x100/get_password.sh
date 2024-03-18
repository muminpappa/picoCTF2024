#!/bin/bash

target=$(echo "${new_pw}" | gdb -q --command=gdb_script ./crackme100 | \
             grep -E 'rsi' | sed -E 's/.*"(.*)"/\1/')

pw='m'

while test ${#pw} -lt ${#target}
do
    next_encr_char=${target:${#pw}:1}

    for o in 0 3 6 9 12 15 18 21 24
    do
        slask="0x$(printf "%x" "'$next_encr_char")"
        slask=$((slask-o))
        slask=$(printf "%x" "$slask")
        guessed_char=$(printf "\x$slask")
        new_pw="${pw}${guessed_char}"

        encr_pw=$(echo "${new_pw}" | gdb -q --command=gdb_script ./crackme100 | \
                      grep -E 'rdi' | sed -E 's/.*"(.*)"/\1/')
        encr_char=${encr_pw:${#pw}:1}
        if test $encr_char == $next_encr_char
        then 
            echo "Found: $guessed_char"
            pw=$new_pw
            break
        fi
    done
done

echo $pw

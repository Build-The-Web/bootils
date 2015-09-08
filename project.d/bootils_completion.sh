_nanny_completion() {
    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _NANNY_COMPLETE=complete $1 ) )
    return 0
}

complete -F _nanny_completion -o default nanny;

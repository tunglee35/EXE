#!/bin/bash
WORKING_DIR="$HOME/code/FPT/EXE/"
SERVER_PORT="8000"
USER_NAME="admin"
PASSWORD="randompass"
session="${1:-session}"
window="${2:-window}"
cd web_app
# pip3 install -r requirements.txt
tmux kill-session -t "$session"
tmux new-session -d  -s "$session"
tmux new-window -t "$session"
for (( i = 0; i < 2; i++ )); do
      tmux split
	tmux select-layout even-vertical
done
	###  Step 2: Run the commands
	# Commands to run
command_list=(
    "streamlit run app.py --server.port $SERVER_PORT"
    "ngrok http $SERVER_PORT --basic-auth='$USER_NAME:$PASSWORD'"
)
for (( i=0; i<${#command_list[@]}; i++ ));
do
    # tmux select-pane -t $i
	command=${command_list[$i]}
	    tmux send-keys -t "$session:1.$i" "echo command is: $command" C-m
		    tmux send-keys -t "$session:1.$i" "$command" C-m
	    done
	    tmux attach-session -t "$session"

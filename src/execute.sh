#!/bin/bash

# Valori predefiniti
models=1
threads=$(nproc)
threads=$((threads - 2))
timeLimit=60

# Parsing degli argomenti con getopts
while getopts "t:m:p:h" opt; do
    case $opt in
        t) timeLimit=$OPTARG ;;   # -t per il limite di tempo
        m) models=$OPTARG ;;      # -m per il numero di modelli
        p) threads=$OPTARG ;;     # -p per il numero di thread
        h)
            echo "Uso: $0 [-t timeLimit] [-m models] [-p threads]"
            exit 1 ;;
        *) 
            echo "Uso: $0 [-t timeLimit] [-m models] [-p threads]"
            exit 1 ;;
    esac
done

# Stampa i valori usati
echo "Eseguo con i seguenti parametri:"
echo "Numero di modelli: $models"
echo "Numero di thread: $threads"
echo "Limite di tempo: $timeLimit"

# Esegui il comando clingo
clingo -n "$models" --parallel-mode "$threads" --time-limit="$timeLimit" lp/* main-ottimizzato.lp

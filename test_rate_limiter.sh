API_URL="http://localhost:8000/hello"
REQUESTS=100
DELAY=0.03

echo "Testing rate limits on $API_URL ($REQUESTS requests, ${DELAY}s delay)"
echo "----------------------------------------"

for i in $(seq 1 $REQUESTS); do
    response=$(curl -i -s -w "\n%{http_code}" $API_URL)
    status_code=$(echo "$response" | tail -n1)

    if [[ $status_code == 200 ]]; then
        color="\033[32m"
    else
        color="\033[31m"
    fi

    printf "\nRequest %d: Status %b%d\033[0m" "$i" "$color" "$status_code"

    echo "$response" | grep -E "X-RateLimit-Remaining|Retry-After"

    [[ $i -lt $REQUESTS ]] && sleep $DELAY
done

echo -e "\n----------------------------------------\nTest completed!"
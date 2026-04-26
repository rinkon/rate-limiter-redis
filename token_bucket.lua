local token_count_key = KEYS[1]
local timestamp_key = KEYS[2]

local refill_rate = tonumber(ARGV[1])
local bucket_capacity = tonumber(ARGV[2])
local now_timestamp = tonumber(ARGV[3])
local required_token = tonumber(ARGV[4])
local ttl = math.floor(2*(bucket_capacity/refill_rate))


local last_request_timestamp = tonumber(redis.call('get', timestamp_key))
if last_request_timestamp == nil then
    last_request_timestamp = now_timestamp
end

local last_av_token_count = tonumber(redis.call('get', token_count_key))
if last_av_token_count == nil then
    last_av_token_count = bucket_capacity
end 

local time_diff = now_timestamp - last_request_timestamp

local current_av_token_count = math.min(bucket_capacity, last_av_token_count + time_diff * refill_rate)
local allowed = current_av_token_count >= required_token

if allowed then
    current_av_token_count = current_av_token_count - required_token
end

redis.call('setex', token_count_key, ttl, current_av_token_count)
redis.call('setex', timestamp_key, ttl, now_timestamp)

return {allowed, current_av_token_count}
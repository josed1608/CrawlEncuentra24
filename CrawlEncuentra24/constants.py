lua_script_paginar = '''
function main(splash, args)
  assert(splash:go(args.url))
  wait_for_element(splash, '.filter_refine_tag_container', 200)
  return splash:html()
end

function wait_for_element(splash, css, maxwait)
    if maxwait == nil then
        maxwait = 10
    end
    local exit = false
    local time_chunk = 0.2
    local time_passed = 0
    while (exit == false)
    do
        local element = splash:select(css)
        if element then
            exit = true
        elseif time_passed >= maxwait then
            exit = true
            error('Timed out waiting for -' .. css)
        else
            splash:wait(time_chunk)
            time_passed = time_passed + time_chunk
        end
    end
end'''

stop_docker_command = 'docker stop crawler'

start_docker_command = 'docker run -p 8050:8050 --rm --name crawler scrapinghub/splash &'

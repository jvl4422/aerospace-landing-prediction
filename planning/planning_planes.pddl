(define (problem landingplanes) (:domain airspace)
; Below we are defining 
(:objects 
ac868 - heavy ;1
ba557 - light ; 3
ua934 - heavy ; 2
ay1339 - light ; +5 4
ba987 - medium
az248 - medium ; + 10
lh920 - heavy
b61107 - medium
sn2105 - heavy ; +15
kl1033 - light
tk1983 - heavy


hthrw - runway


)

(:init
    ;todo: put the initial state's facts and numeric values here
    ; I want to use the "at time" to model when a plane can make a landing approach
    ; But I have yet to find a planner that I can get to work that supports timed initial literals
    ; but without timed initial literals this problem becomes arbitrarily easy because planes will just land
    ; from smallest to largest
    (rwystatus-empty)
    (canland ac868)
    (canland ba557)
    (canland ua934)
    (= (landing-possible-at ay1339) 6)
    (= (landing-possible-at ba987) 6)
    (= (landing-possible-at az248) 10)
    (= (landing-possible-at lh920) 10)
    (= (landing-possible-at b61107) 10)
    (= (landing-possible-at sn2105) 16)
    (= (landing-possible-at kl1033) 16)
    (= (landing-possible-at tk1983) 16)
    (= (total-time) 0)

)

(:goal 
(and 
    (landed ac868 hthrw)
    (landed ba557 hthrw)
    (landed ua934 hthrw)
    (landed ay1339 hthrw)
    (landed ba987 hthrw)
    (landed az248 hthrw)
    (landed lh920 hthrw)
    (landed b61107 hthrw)
    (landed sn2105 hthrw)
    (landed kl1033 hthrw)
    (landed tk1983 hthrw)
)

)



;un-comment the following line if metric is needed
(:metric minimize (total-time))
)
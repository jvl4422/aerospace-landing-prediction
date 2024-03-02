(define (problem landingplanes) (:domain airspace)
; Below we are defining 
(:objects 
worldtime - clock
dhHerc - light
embPhen100 - light
hthrw - runway


)

(:init
    ;todo: put the initial state's facts and numeric values here
    ; I want to use the "at time" to model when a plane can make a landing approach
    ; But I have yet to find a planner that I can get to work that supports timed initial literals
    ; but without timed initial literals this problem becomes arbitrarily easy because planes will just land
    ; from smallest to largest
    (rwystatus-empty)
    (canland embPhen100)
    (= (landing-possible-at dhHerc) 1)
    (= (total-time) 0)

)

(:goal 
(and 
    (landed dhHerc hthrw)
    (landed embPhen100 hthrw)
)

)



;un-comment the following line if metric is needed
(:metric minimize (total-time))
)
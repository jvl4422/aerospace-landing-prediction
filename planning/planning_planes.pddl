(define (problem landingplanes) (:domain airspace)
; Below we are defining 
(:objects 
dhHerc - light
embPhen100 - light
hthrw - runway


)

(:init
    ;todo: put the initial state's facts and numeric values here
    (rwystatus-empty)
)

(:goal 
(and 
    (landed dhHerc hthrw)
    (landed embPhen100 hthrw)
)

)



;un-comment the following line if metric is needed
;(:metric minimize (???))
)
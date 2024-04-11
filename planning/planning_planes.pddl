(define (problem landingplanes) (:domain airspace)
; Below we are defining 
(:objects 
ba1327 - medium ;
ju210 - medium ; 
vs118 - heavy ; + 5
ba343 - medium ; +10 
lh906 - medium ; 
ei162 - medium ; 
aa80 - heavy ; + 15
ba266 - heavy
ba697 - medium ; 
tp1532 - medium
ey19 - super;
aa134 - heavy; ; +20
ah2474 - medium
vy8960 - medium
sk531 - medium ; + 25
ba48 - heavy ; +30
ba553 - medium 
ba919 - heavy
lx332 - medium
ba122 - heavy
ba359 - medium ; + 35
ba763 - medium
ba1307 - medium
ba118 - heavy
ei712 - medium
ba361 - medium ; +40
ba541 - medium
ba1421 - medium
lm653 - light
ba260 - heavy
dl20 - heavy ; +45
ba1443 - medium 
qr3 - super
ac860 -heavy ; +50
ba777 - medium
ba276 - heavy 
ba156 - heavy ; +55
ba421 - medium
ei164 - medium
ba373 - medium ; +60
ba459 - medium






hthrw - runway


)

(:init
    ;todo: put the initial state's facts and numeric values here
    ; I want to use the "at time" to model when a plane can make a landing approach
    ; But I have yet to find a planner that I can get to work that supports timed initial literals
    ; but without timed initial literals this problem becomes arbitrarily easy because planes will just land
    ; from smallest to largest
    (rwystatus-empty)
    (canland ba1327)
    (canland ju210)
    (= (landing-possible-at vs118) 2)
    (= (landing-possible-at ba343) 2)
    (= (landing-possible-at lh906) 2)
    (= (landing-possible-at ei162) 2)
    (= (landing-possible-at aa80) 6)
    (= (landing-possible-at ba266) 6)
    (= (landing-possible-at tp1532) 6)
    (= (landing-possible-at ey19) 6)
    (= (landing-possible-at aa134) 10)
    (= (landing-possible-at ah2474) 10)
    (= (landing-possible-at vy8960) 10)
    (= (landing-possible-at sk531) 13)
    (= (landing-possible-at ba48) 14)
    (= (landing-possible-at ba553) 14)
    (= (landing-possible-at ba919) 14)
    (= (landing-possible-at lx332) 14)
    (= (landing-possible-at ba122) 14)
    (= (landing-possible-at ba359) 18)
    (= (landing-possible-at ba763) 18)
    (= (landing-possible-at ba1307) 18)
    (= (landing-possible-at ba118) 18)
    (= (landing-possible-at ei712) 18)
    (= (landing-possible-at ba359) 18)
    (= (landing-possible-at ba361) 23)
    (= (landing-possible-at ba541) 23)
    (= (landing-possible-at ba1421) 23)
    (= (landing-possible-at lm653) 23)
    (= (landing-possible-at ba260) 23)
    (= (landing-possible-at dl20) 28)
    (= (landing-possible-at ba1443) 28)
    (= (landing-possible-at qr3) 28)
    (= (landing-possible-at ac860) 31)
    (= (landing-possible-at ba777) 31)
    (= (landing-possible-at ba276) 31)
    (= (landing-possible-at ba156) 34)
    (= (landing-possible-at ba421) 34)
    (= (landing-possible-at ei164) 34)
    (= (landing-possible-at ba156) 34)
    (= (landing-possible-at ba373) 38)
    (= (landing-possible-at ba459) 34)
    (= (total-time) 0)

)

(:goal 
(and 
    (landed vs118 hthrw)
    (landed ba343 hthrw)
    (landed lh906 hthrw)
    (landed ei162 hthrw)
    (landed ba1327 hthrw)
    (landed ju210 hthrw)
    (landed aa80 hthrw)
    (landed ba266 hthrw)
    (landed tp1532 hthrw)
    (landed ey19 hthrw)
    (landed aa134 hthrw)
    (landed ah2474 hthrw)
    (landed vy8960 hthrw)
    (landed sk531 hthrw)
    (landed ba48 hthrw)
    (landed ba553 hthrw)
    (landed ba919 hthrw)
    (landed lx332 hthrw)
    (landed ba122 hthrw)
    (landed ba359 hthrw)
    (landed ba763 hthrw)
    (landed ba1307 hthrw)
    (landed ba118 hthrw)
    (landed ei712 hthrw)
    (landed ba361 hthrw)
    (landed ba541 hthrw)
    (landed ba1421 hthrw)
    (landed lm653 hthrw)
    (landed ba260 hthrw)
    (landed dl20 hthrw)
    (landed ba1443 hthrw)
    (landed qr3 hthrw)
    (landed ac860 hthrw)
    (landed ba777 hthrw)
    (landed ba276 hthrw)
    (landed ba156 hthrw)
    (landed ba421 hthrw)
    (landed ei164 hthrw)
    (landed ba373 hthrw)
    (landed ba459 hthrw)
)

)



;un-comment the following line if metric is needed
(:metric minimize (total-time))
)
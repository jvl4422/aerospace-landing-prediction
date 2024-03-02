(define (domain airspace)

;remove requirements that are not needed
; Typing means types
(:requirements :strips :durative-actions :typing :conditional-effects :equality)

(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    runway airplane - object 
    ; Following ICAO categories..... 
    light medium heavy super - airplane

)

; un-comment following line if constants are needed
;(:constants )

; Predicates apply to a specific type of object, or to all objects. 
; Predicates are either true or false at any point in a plan and when not declared are assumed to be false
(:predicates ;todo: define predicates here
        (landed ?pln - airplane ?rwy - runway)
        (rwystatus-empty)
        (rwylight)
        ;(holding ?arm - locatable ?cupcake - locatable)
    ;(arm-empty)
        

)


(:functions ;todo: define numeric functions here
)

(:durative-action land-light-light
    :parameters (
      ?pln - airplane
      ?rwy - runway
    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwylight)))
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwylight)))
)

; I don't think this needs to be a durative action as the plane will be landing first regardless because this is
; the first action that can be taken. Also, there is no difference between light vs medium vs heavy vs super landing times
; when they don't land behind another plane. 
(:durative-action land-init-light
    :parameters (
      ?pln - light
      ?rwy - runway
    )
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwystatus-empty))
        )
    :effect (and 
        (at end (landed ?pln ?rwy))
        (at end (rwylight))
        (at end (not (rwystatus-empty))))
)

)
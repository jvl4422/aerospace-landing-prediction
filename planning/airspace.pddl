(define (domain airspace)

;remove requirements that are not needed
; Typing means types
(:requirements :strips :durative-actions :typing :conditional-effects :equality)

(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    runway airplane clock - object 
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
        (canland ?pln - airplane)
)


(:functions ;todo: define numeric functions here
  ; lets see if we can do inheritance
  ; represents what time a plane is allowed to land if we cannot use timed initial literals
  ; looks like I do not have to give this a type but I can just say minimize / maximize at the end
  (total-time)
  (landing-possible-at ?pln - airplane)
)

; YAY THIS DID NOT APPEAR TO BREAK EVERYTHING
(:durative-action now-landing-possible
    :parameters (
      ?pln - airplane
    )
    :duration (= ?duration 1)
    :condition (and 
        (at start (not (canland ?pln)))
        (at start (>= (landing-possible-at ?pln) (total-time)))
    )
    :effect (and 
        (at end (canland ?pln))
        (at end (increase(total-time) 1))
    )
)



(:durative-action land-light-light
    :parameters (
      ?pln - light
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwylight))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwylight))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 2))
              )
)

; There is no difference between light vs medium vs heavy vs super landing times
; when they don't land behind another plane. 
; But we do need to categorize so we can set the correct flag for most recently landed
(:durative-action land-init-light
    :parameters (
      ?pln - light
      ?rwy - runway
    )
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwystatus-empty))
        (at start (canland ?pln))
        )
    :effect (and 
        (at end (landed ?pln ?rwy))
        (at end (rwylight))
        (at end (not (rwystatus-empty)))
        (at end (not (canland ?pln)))
        (at end (increase(total-time) 2))
        )

)

)
(define (domain airspace)

;remove requirements that are not needed
; Typing means types
(:requirements :strips :durative-actions :typing :conditional-effects :equality)

(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    runway airplane - object 
    ; Following ICAO categories..... 
    light medium heavy super - airplane

)

; Predicates apply to a specific type of object, or to all objects. 
; Predicates are either true or false at any point in a plan and when not declared are assumed to be false
(:predicates ;todo: define predicates here
        (landed ?pln - airplane ?rwy - runway)
        (canland ?pln - airplane)
        (rwystatus-empty)
        (rwylight)
        (rwymedium)
        (rwyheavy)
        (rwysuper)
        
)


(:functions ;todo: define numeric functions here
  ; lets see if we can do inheritance
  ; represents what time a plane is allowed to land if we cannot use timed initial literals
  ; looks like I do not have to give this a type but I can just say minimize / maximize at the end
  ; the landing possible at is my workaround for no support of timed literals
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
        (at start (<= (landing-possible-at ?pln) (total-time)))
    )
    :effect (and 
        (at end (canland ?pln))
        
    )
)
; Do not increase total time at the end because technically no time should have passed


; LANDING INITIALS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
        (at start (< (total-time) 1))
        )
    :effect (and 
        (at end (landed ?pln ?rwy))
        (at end (rwylight))
        (at end (not (rwystatus-empty)))
        (at end (not (canland ?pln)))
        (at end (increase(total-time) 1))
        )

)

(:durative-action land-init-medium
    :parameters (
      ?pln - medium
      ?rwy - runway
    )
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwystatus-empty))
        (at start (canland ?pln))
        (at start (< (total-time) 1))
        )
    :effect (and 
        (at end (landed ?pln ?rwy))
        (at end (rwymedium))
        (at end (not (rwystatus-empty)))
        (at end (not (canland ?pln)))
        (at end (increase(total-time) 1))
        )

)

(:durative-action land-init-heavy
    :parameters (
      ?pln - heavy
      ?rwy - runway
    )
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwystatus-empty))
        (at start (canland ?pln))
        (at start (< (total-time) 1))
        )
    :effect (and 
        (at end (landed ?pln ?rwy))
        (at end (rwyheavy))
        (at end (not (rwystatus-empty)))
        (at end (not (canland ?pln)))
        (at end (increase(total-time) 1))
        )

)

(:durative-action land-init-super
    :parameters (
      ?pln - super
      ?rwy - runway
    )
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwystatus-empty))
        (at start (canland ?pln))
        (at start (< (total-time) 1))
        )
    :effect (and 
        (at end (landed ?pln ?rwy))
        (at end (rwysuper))
        (at end (not (rwystatus-empty)))
        (at end (not (canland ?pln)))
        (at end (increase(total-time) 1))
        )

)

; LANDING SEQUENTIAL ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
              (at end (increase(total-time) 1))
              )
)

; light medium does not require extra time
(:durative-action land-light-medium
    :parameters (
      ?pln - medium
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
              (at end (rwymedium))
              (at end (not (rwylight)))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 1))
              )
)

(:durative-action land-medium-light
    :parameters (
      ?pln - light
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 3)
    :condition (and 
        (at start (rwymedium))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwylight))
              (at end (not (rwymedium)))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 3))
              )
)

(:durative-action land-medium-medium
    :parameters (
      ?pln - medium
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwymedium))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwymedium))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 1))
              )
)

(:durative-action land-light-heavy
    :parameters (
      ?pln - heavy
      ?rwy - runway

    )
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwylight))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwyheavy))
              (at end (not (rwylight)))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 1))
              )
)

(:durative-action land-heavy-light
    :parameters (
      ?pln - light
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 3)
    :condition (and 
        (at start (rwyheavy))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwylight))
              (at end (not (rwyheavy)))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 3))
              )
)

(:durative-action land-light-super
    :parameters (
      ?pln - super
      ?rwy - runway

    )
    :duration (= ?duration 4)
    :condition (and 
        (at start (rwylight))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwysuper))
              (at end (not (rwylight)))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 4))
              )
)

(:durative-action land-super-light
    :parameters (
      ?pln - super
      ?rwy - runway

    )
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwysuper))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwylight))
              (at end (not (rwysuper)))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 1))
              )
)


(:durative-action land-medium-heavy
    :parameters (
      ?pln - heavy
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwymedium))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwyheavy))
              (at end (not (rwymedium)))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 1))
              )
)


(:durative-action land-heavy-medium
    :parameters (
      ?pln - medium
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 2)
    :condition (and 
        (at start (rwyheavy))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwymedium))
              (at end (not (rwyheavy)))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 2))
              )
)

(:durative-action land-medium-super
    :parameters (
      ?pln - super
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwymedium))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwysuper))
              (at end (not (rwymedium)))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 1))
              )
)

(:durative-action land-super-medium
    :parameters (
      ?pln - medium
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 3)
    :condition (and 
        (at start (rwysuper))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwymedium))
              (at end (not (rwysuper)))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 3))
              )
)

(:durative-action land-heavy-heavy
    :parameters (
      ?pln - heavy
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwyheavy))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwyheavy))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 1))
              )
)

(:durative-action land-heavy-super
    :parameters (
      ?pln - super
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 1)
    :condition (and 
        (at start (rwyheavy))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (not (rwyheavy)))
              (at end (rwysuper))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 1))
              )
)

(:durative-action land-super-heavy
    :parameters (
      ?pln - heavy
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 2)
    :condition (and 
        (at start (rwysuper))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (not (rwysuper)))
              (at end (rwyheavy))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 2))
              )
)

(:durative-action land-super-super
    :parameters (
      ?pln - super
      ?rwy - runway

    )
    ; 45 seconds / 60 seconds = 0.76 of a minute
    ; because I am not sure if I am allowed to use decimals, we will just call it one minute
    :duration (= ?duration 2)
    :condition (and 
        (at start (rwysuper))
        (at start (canland ?pln))
        )
        
    ; I feel like the double at end condition is longer than it needs to be
    :effect
        ( and (at end  (landed ?pln ?rwy))
              (at end (rwysuper))
              (at end (not (canland ?pln)))
              (at end (increase(total-time) 2))
              )
)

)

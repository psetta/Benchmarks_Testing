#lang racket

;num + num -> vector de números aleatorios
(define (vector_entrada rang num)
  (build-vector num (lambda(x) (random rang))))

;vector -> vector de números repetidos
(define (elementos_iguales vector)
  (define d (make-hash))
  (vector-map (lambda(x) (hash-update! d x add1 0)) vector)
  (vector-filter (lambda(z) (> (hash-ref d z) 1)) vector)
  )

(define rang (string->number (vector-ref (current-command-line-arguments) 0)))
(define numero (string->number (vector-ref (current-command-line-arguments) 1)))

;(displayln v)
(void (elementos_iguales (vector_entrada rang numero)))
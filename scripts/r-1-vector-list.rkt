#lang racket

;num + num -> vector de números aleatorios
(define (lista_entrada rang num)
  (vector->list (build-vector num (lambda(x) (random rang)))))

;vector -> vector de números repetidos
(define (elementos_iguales lista)
  (define d (make-hash))
  (map (lambda(x) (hash-update! d x add1 0)) lista)
  (filter (lambda(z) (> (hash-ref d z) 1)) lista)
  )

(define rang (string->number (vector-ref (current-command-line-arguments) 0)))
(define numero (string->number (vector-ref (current-command-line-arguments) 1)))

;(displayln v)
(void (elementos_iguales (lista_entrada rang numero)))
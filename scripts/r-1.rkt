#lang racket

(define (lista_entrada rango num)
  (map (lambda (x) (random rango))
       (make-list num 0)))

;DEFINIMOS A FUNCIÓN ENCARGADA DE MOSTRAR OS ELEMENTOS REPETIDOS DA LISTA

(define (elementos_iguales lista)
  (define d (make-hash))
  (map (lambda(x) (hash-update! d x add1 0)) lista)
  (filter (lambda(z) (> (hash-ref d z) 1)) lista)
  )

(define rang (string->number (vector-ref (current-command-line-arguments) 0)))
(define numero (string->number (vector-ref (current-command-line-arguments) 1)))

(void (elementos_iguales (lista_entrada rang numero)))
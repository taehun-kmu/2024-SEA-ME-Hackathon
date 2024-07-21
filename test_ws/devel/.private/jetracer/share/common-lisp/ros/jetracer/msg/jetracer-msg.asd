
(cl:in-package :asdf)

(defsystem "jetracer-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "jetRacerCar" :depends-on ("_package_jetRacerCar"))
    (:file "_package_jetRacerCar" :depends-on ("_package"))
  ))
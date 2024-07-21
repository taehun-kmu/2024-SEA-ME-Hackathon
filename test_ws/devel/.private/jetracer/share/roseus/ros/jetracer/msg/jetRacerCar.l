;; Auto-generated. Do not edit!


(when (boundp 'jetracer::jetRacerCar)
  (if (not (find-package "JETRACER"))
    (make-package "JETRACER"))
  (shadow 'jetRacerCar (find-package "JETRACER")))
(unless (find-package "JETRACER::JETRACERCAR")
  (make-package "JETRACER::JETRACERCAR"))

(in-package "ROS")
;;//! \htmlinclude jetRacerCar.msg.html


(defclass jetracer::jetRacerCar
  :super ros::object
  :slots (_steerAngle _throttle ))

(defmethod jetracer::jetRacerCar
  (:init
   (&key
    ((:steerAngle __steerAngle) 0.0)
    ((:throttle __throttle) 0.0)
    )
   (send-super :init)
   (setq _steerAngle (float __steerAngle))
   (setq _throttle (float __throttle))
   self)
  (:steerAngle
   (&optional __steerAngle)
   (if __steerAngle (setq _steerAngle __steerAngle)) _steerAngle)
  (:throttle
   (&optional __throttle)
   (if __throttle (setq _throttle __throttle)) _throttle)
  (:serialization-length
   ()
   (+
    ;; float32 _steerAngle
    4
    ;; float32 _throttle
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _steerAngle
       (sys::poke _steerAngle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _throttle
       (sys::poke _throttle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _steerAngle
     (setq _steerAngle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _throttle
     (setq _throttle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get jetracer::jetRacerCar :md5sum-) "aff191fd10fed555ff6297c6aea6a03a")
(setf (get jetracer::jetRacerCar :datatype-) "jetracer/jetRacerCar")
(setf (get jetracer::jetRacerCar :definition-)
      "float32 steerAngle
float32 throttle

")



(provide :jetracer/jetRacerCar "aff191fd10fed555ff6297c6aea6a03a")



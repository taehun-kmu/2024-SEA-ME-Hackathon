; Auto-generated. Do not edit!


(cl:in-package jetracer-msg)


;//! \htmlinclude jetRacerCar.msg.html

(cl:defclass <jetRacerCar> (roslisp-msg-protocol:ros-message)
  ((steerAngle
    :reader steerAngle
    :initarg :steerAngle
    :type cl:float
    :initform 0.0)
   (throttle
    :reader throttle
    :initarg :throttle
    :type cl:float
    :initform 0.0))
)

(cl:defclass jetRacerCar (<jetRacerCar>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <jetRacerCar>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'jetRacerCar)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name jetracer-msg:<jetRacerCar> is deprecated: use jetracer-msg:jetRacerCar instead.")))

(cl:ensure-generic-function 'steerAngle-val :lambda-list '(m))
(cl:defmethod steerAngle-val ((m <jetRacerCar>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader jetracer-msg:steerAngle-val is deprecated.  Use jetracer-msg:steerAngle instead.")
  (steerAngle m))

(cl:ensure-generic-function 'throttle-val :lambda-list '(m))
(cl:defmethod throttle-val ((m <jetRacerCar>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader jetracer-msg:throttle-val is deprecated.  Use jetracer-msg:throttle instead.")
  (throttle m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <jetRacerCar>) ostream)
  "Serializes a message object of type '<jetRacerCar>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'steerAngle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'throttle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <jetRacerCar>) istream)
  "Deserializes a message object of type '<jetRacerCar>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'steerAngle) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'throttle) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<jetRacerCar>)))
  "Returns string type for a message object of type '<jetRacerCar>"
  "jetracer/jetRacerCar")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'jetRacerCar)))
  "Returns string type for a message object of type 'jetRacerCar"
  "jetracer/jetRacerCar")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<jetRacerCar>)))
  "Returns md5sum for a message object of type '<jetRacerCar>"
  "aff191fd10fed555ff6297c6aea6a03a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'jetRacerCar)))
  "Returns md5sum for a message object of type 'jetRacerCar"
  "aff191fd10fed555ff6297c6aea6a03a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<jetRacerCar>)))
  "Returns full string definition for message of type '<jetRacerCar>"
  (cl:format cl:nil "float32 steerAngle~%float32 throttle~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'jetRacerCar)))
  "Returns full string definition for message of type 'jetRacerCar"
  (cl:format cl:nil "float32 steerAngle~%float32 throttle~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <jetRacerCar>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <jetRacerCar>))
  "Converts a ROS message object to a list"
  (cl:list 'jetRacerCar
    (cl:cons ':steerAngle (steerAngle msg))
    (cl:cons ':throttle (throttle msg))
))

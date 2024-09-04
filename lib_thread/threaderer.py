# MORE THREADS!!! #

from time import sleep
import _thread

counter = 1

def thread_function(my_number):
    # counter += 1
    # print (counter)
    print ("hello")
    for i in range(2):
        print(my_number)
        # print(my_number," - ",i," time, indent: ",_thread.get_ident(), "size", _thread.stack_size())
        # if my_number < 3:
        #     break
        sleep(1)

    print ("bye bye! ", my_number)    
    _thread.exit()


def thread_blink(blink_pin):
    while True:
        blink_pin.value(0) # LED on
        sleep(1)
        blink_pin.value(1) # LED off
        sleep(1)


_thread.start_new_thread(thread_blink, (led,))
counter += 1

for i in range(48):
    _thread.start_new_thread(thread_function, (counter,))
    counter += 1
    # print (counter)
    sleep(0.02)


# exec(open("threads/threaderer.py").read())

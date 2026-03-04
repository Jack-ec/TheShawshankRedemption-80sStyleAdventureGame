from tkinter import *
from tkinter import ttk
import GameObject

command_widget = None
image_label = None
description_widget = None
inventory_widget = None
north_button = None
south_button = None
east_button = None
west_button = None
root = None

rock_hammer_found = False
talked_to_red = False
tunnel_dug = False
refresh_location = True
refresh_objects_visible = True

current_location = 1
end_of_game = False

bible = GameObject.GameObject("Holy Bible", 3, True, True, False,
                              "This is the Holy Bible. It contains wisdom and solutions to problems for many. Always remember that 'salvation lay within'.")
cigarettes = GameObject.GameObject("pack of cigarettes", 4, True, True, False,
                                   "cigarettes, cigars and alcohol are a form of currency in Shawshank Prison. You better hold on to these.")
whiskey = GameObject.GameObject("bottle of whiskey", 6, True, True, False,
                                "cigarettes, cigars and alcohol are a form of currency in Shawshank Prison. You better hold on to these.")
cigars = GameObject.GameObject("package of cigars", 7, True, True, False,
                               "cigarettes, cigars and alcohol are a form of currency in Shawshank Prison. You better hold on to these.")
red = GameObject.GameObject("Red", 9, False, True, False,
                            "Red is the guy in shawshank prison who can get stuff. whiskey, playing cards you name it. He might even have something that can help you escape.")
rock_hammer = GameObject.GameObject("Rock Hammer", 3, True, False, False,
                                    "This rock hammer was hidden in a bible. You could probably dig a tunnel with this but you would need something to cover the hole with.")
poster = GameObject.GameObject("Poster", 9, True, False, False, "You could cover a tunnel with this poster")
game_objects = [bible, cigarettes, whiskey, cigars, red, rock_hammer, poster]


def perform_command(verb, noun):
    if verb == "GO":
        perform_go_command(noun)
    elif verb == "N" or verb == "S" or verb == "E" or verb == "W":
        perform_go_command(verb)
    elif verb == "NORTH" or verb == "SOUTH" or verb == "EAST" or verb == "WEST":
        perform_go_command(noun)
    elif verb == "GET":
        perform_get_command(noun)
    elif verb == "PUT":
        perform_put_command(noun)
    elif verb == "LOOK":
        perform_look_command(noun)
    elif verb == "READ":
        perform_read_command(noun)
    elif verb == "OPEN":
        perform_open_command(noun)
    elif verb == 'STATE':
        set_current_state()
    elif verb == 'TALK':
        perform_talk_command(noun[3:] if noun.startswith("TO ") else noun)
    elif verb == 'USE':
        perform_use_command(noun)
    elif verb == 'BUY':
        perform_buy_command()
    else:
        print_to_description("huh?")


def perform_go_command(direction):
    global current_location
    global refresh_location

    if direction == "N" or direction == "NORTH":
        new_location = get_location_to_north()
    elif direction == "S" or direction == "SOUTH":
        new_location = get_location_to_south()
    elif direction == "E" or direction == "EAST":
        new_location = get_location_to_east()
    elif direction == "W" or direction == "WEST":
        new_location = get_location_to_west()
    else:
        new_location = 0

    if new_location == 0:
        print_to_description("You can't go that way!")
    else:
        current_location = new_location
        refresh_location = True


def perform_get_command(object_name):
    global refresh_objects_visible
    game_object = get_game_object(object_name)

    if game_object is not None:
        if game_object.location != current_location and not game_object.carried:
            print_to_description("You don't see one of those here!")
        elif not game_object.movable:
            print_to_description("You can't pick it up!")
        elif game_object.carried:
            print_to_description("You are already carrying it")
        else:
            game_object.carried = True
            game_object.visible = False
            refresh_objects_visible = True
            print_to_description("You pick up the " + game_object.name + ".")
    else:
        print_to_description("You don't see one of those here!")


def perform_use_command(object_name):
    global tunnel_dug
    global refresh_objects_visible

    game_object = get_game_object(object_name)

    if game_object == rock_hammer:
        if not rock_hammer.carried:
            print_to_description("You aren't carrying the rock hammer.")
        elif current_location != 1:
            print_to_description("There's nothing useful to do with that here.")
        elif tunnel_dug:
            print_to_description("You've already dug the tunnel.")
        else:
            tunnel_dug = True
            refresh_objects_visible = True
            print_to_description(
                "You chip away at the wall with the rock hammer. After hours of work, you've dug a tunnel behind your cell wall. Now you need something to cover the hole.")
    else:
        print_to_description("You can't use that.")


def perform_buy_command():
    if current_location == 9:
        if not talked_to_red:
            print_to_description("You should probably talk to Red first.")
        elif cigarettes.carried and whiskey.carried and cigars.carried:
            poster.carried = True
            cigarettes.carried = False
            whiskey.carried = False
            cigars.carried = False
            print_to_description("Pleasure doing buisness with ya. Here's your poster.")
        else:
            print_to_description("Sorry man, I can't give you the poster unless you can pay full price.")
    else:
        print_to_description("huh?")


def perform_put_command(object_name):
    global refresh_objects_visible
    game_object = get_game_object(object_name)

    if game_object is not None:
        if not game_object.carried:
            print_to_description("You are not carrying one of those.")
        else:
            game_object.location = current_location
            game_object.carried = False
            game_object.visible = True
            refresh_objects_visible = True
    else:
        print_to_description("You are not carrying one of those!")


def perform_talk_command(object_name):
    global talked_to_red
    game_object = get_game_object(object_name)

    if game_object == red and current_location == 9:
        talked_to_red = True
        print_to_description(
            "Hey there, I got this poster that you ordered. It will cost you a pack of cigarettes, a bottle of whiskey and a package of cigars.")
    else:
        print_to_description("huh?")


def perform_look_command(object_name):
    game_object = get_game_object(object_name)

    if game_object is not None:

        if game_object.carried or (game_object.visible and game_object.location == current_location):
            print_to_description(game_object.description)
        else:
            print_to_description("You can't see one of those!")
    else:
        print_to_description("huh?")


def perform_read_command(object_name):
    game_object = get_game_object(object_name)

    if game_object is not None:
        if game_object == bible:
            if bible.carried:
                print_to_description(
                    "Mark 13:35: Watch ye, therefore, for ye not know when the master of the house cometh.")

        else:
            if not game_object.visible and not game_object.carried:
                print_to_description("You can't read what you can't see, silly!")
            elif game_object.location != current_location:
                print_to_description("You can't read what you can't see, silly!")
            else:
                print_to_description("There is no text on it")
    else:
        print_to_description("I am not sure which " + object_name + " you are refering to")


def perform_open_command(object_name):
    global rock_hammer_found
    global refresh_location
    global refresh_objects_visible

    game_object = get_game_object(object_name)

    if game_object is None:
        if object_name == "":
            # generic OPEN
            refresh_location = True
            refresh_objects_visible = True
        else:
            print_to_description("You can't open that")
        return

    if game_object == bible and not rock_hammer_found:
        rock_hammer.location = current_location
        rock_hammer.visible = True
        rock_hammer_found = True
        bible.description = "It is empty"
        refresh_objects_visible = True
    elif game_object == cigarettes:
        print_to_description("There are cigarettes in the pack of cigarettes. What did you think there would be?")
    elif game_object == whiskey:
        print_to_description("There is whiskey inside the bottle. But you gave up drinking.")
    elif game_object == cigars:
        print_to_description("You don't want to open those. They are worth more if the package is sealed")
    else:
        print_to_description("You can't open that")


def describe_current_location():
    ## description of all locations
    if current_location == 1:
        print_to_description(
            "\n\nYou are in your prison cell. all you can see are your bed and the dark stone walls that surround you and the light from the moon pouring in from your barred window. You severely want to escape. You might be able to tunnel through the wall if you found some tools.")
    elif current_location == 2:
        print_to_description("You are in the cell block corridor. What is that up ahead?")
    elif current_location == 3:
        print_to_description(
            "You are in Brooks Hatlen's memorial library. You sure sent a lot of letters to get this place built. Why don't you go look at some books?")
    elif current_location == 4:
        print_to_description("You are in the prison courtyard. Whats that on the ground?")
    elif current_location == 5:
        print_to_description("you are in a prison hallway.")
    elif current_location == 6:
        print_to_description("You are in the Shawshank Prison showers.")
    elif current_location == 7:
        print_to_description(
            "You are in the prison laundry room. You have to be careful not to get the detergent in your eyes because it could blind you.")
    elif current_location == 8:
        print_to_description("You are in a prison hallway.")
    elif current_location == 9:
        print_to_description(
            "You're in Reds Workshop. You should go and talk to red to see if he has any goods for you.")
    elif current_location == 10:
        if not poster.carried and poster.location == 1:
            print_to_description(
                "You have dug an escape hole in your cell wall and covered it with the poster. How clever.")
        else:
            print_to_description(
                "You have dug a hole in your cell wall with the rock hammer. I hope you didn't forget to do something?")
    elif current_location == 11:
        print_to_description(
            "You are in the the sewage pipes. You have to crawl through 500 yards of foulness, that's the length of 5 football fields. But it will all be worth it once you are free!")
    elif current_location == 12:
        if not poster.carried and poster.location == 1:
            print_to_description("You have escaped undetected! You decide to move to Zihuatanejo, Mexico. ")
            print_to_description("GAME OVER.")
    else:
        print_to_description("unknown location:" + str(current_location))


def set_current_image():
    if current_location == 1:
        image_label.img = PhotoImage(file='res/prison cell.gif')
    elif current_location == 2:
        image_label.img = PhotoImage(file='res/prison hallway 2.gif')
    elif current_location == 3:
        image_label.img = PhotoImage(file='res/brooks hatlen library.gif')
    elif current_location == 4:
        image_label.img = PhotoImage(file='res/prison courtyard.gif')
    elif current_location == 5:
        image_label.img = PhotoImage(file='res/prison hallway 5.gif')
    elif current_location == 6:
        image_label.img = PhotoImage(file='res/showers.gif')
    elif current_location == 7:
        image_label.img = PhotoImage(file='res/laundry.gif')
    elif current_location == 8:
        image_label.img = PhotoImage(file='res/prison hallway 8.gif')
    elif current_location == 9:
        image_label.img = PhotoImage(file='res/workshop.gif')
    elif current_location == 10:
        image_label.img = PhotoImage(file='res/escape tunnel.gif')
    elif current_location == 11:
        image_label.img = PhotoImage(file='res/sewerpipe.gif')
    elif current_location == 12:
        if not poster.carried and poster.location == 1:
            image_label.img = PhotoImage(file='res/Freedom.gif')
        else:
            image_label.img = PhotoImage(file='res/solitary.gif')
    else:
        image_label.img = PhotoImage(file='res/blank-1.gif')

    image_label.config(image=image_label.img)


def get_location_to_north():
    if current_location == 1:
        return 2
    elif current_location == 2:
        return 3
    elif current_location == 4:
        return 5
    elif current_location == 5:
        return 6
    elif current_location == 7:
        return 8
    elif current_location == 8:
        return 9
    else:
        return 0


def get_location_to_south():
    if current_location == 3:
        return 2
    elif current_location == 2:
        return 1
    elif current_location == 6:
        return 5
    elif current_location == 5:
        return 4
    elif current_location == 9:
        return 8
    elif current_location == 8:
        return 7
    elif current_location == 11:
        return 12
    else:
        return 0


def get_location_to_west():
    if current_location == 2:
        return 5
    elif current_location == 5:
        return 8
    elif current_location == 11:
        return 10
    elif current_location == 10:
        return 1
    else:
        return 0


def get_location_to_east():
    if current_location == 8:
        return 5
    elif current_location == 5:
        return 2
    elif current_location == 1:
        if tunnel_dug:
            return 10
        else:
            return 0
    elif current_location == 10:
        return 11
    else:
        return 0


def handle_special_condition():
    global end_of_game

    if current_location == 12 and (poster.carried or poster.location != 1):
        print_to_description(
            "You were caught because you forgot to place the poster over your escape hole. You carry the rest of your sentence out in solitary confinement")
        print_to_description("GAME OVER")
        end_of_game = True


def print_to_description(output, user_input=False):
    description_widget.config(state='normal')
    description_widget.insert(END, output)
    if user_input:
        description_widget.tag_add("blue_text", CURRENT + " linestart", END + "-1c")
        description_widget.tag_configure("blue_text", foreground='blue')
    description_widget.insert(END, '\n')
    description_widget.config(state='disabled')
    description_widget.see(END)


def get_game_object(object_name):
    sought_object = None
    for current_object in game_objects:
        if current_object.name.upper() == object_name:
            sought_object = current_object
            break
    return sought_object


def describe_current_visible_objects():
    visible_objects = [
        obj.name for obj in game_objects
        if obj.location == current_location and obj.visible and not obj.carried
    ]
    object_list = ",".join(visible_objects)
    print_to_description("You see: " + (object_list + "." if visible_objects else "nothing special."))


def describe_current_inventory():
    carried_objects = [obj.name for obj in game_objects if obj.carried]

    if carried_objects:
        inventory = "You are carrying:\n" + "\n".join(carried_objects)
    else:
        inventory = "You are carrying: nothing"

    inventory_widget.config(state="normal")
    inventory_widget.delete(1.0, END)
    inventory_widget.insert(1.0, inventory)
    inventory_widget.config(state="disabled")


def build_interface():
    global command_widget
    global image_label
    global description_widget
    global inventory_widget
    global north_button
    global south_button
    global east_button
    global west_button
    global root

    root = Tk()
    root.title("The Shawshank Redemption")
    root.resizable(False, False)

    # Scale only the font, let widget char units follow naturally
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    s = min(screen_w / 1280, screen_h / 1080)
    base_font = ("Helvetica", max(8, int(11 * s)))
    small_font = ("Helvetica", max(7, int(10 * s)))
    btn_font = ("Helvetica", max(8, int(11 * s)), "bold")
    px = lambda n: max(1, int(n * s))

    image_label = ttk.Label(root)
    image_label.grid(row=0, column=0, columnspan=5, padx=px(30), pady=px(15), sticky="")

    description_widget = Text(root, width=50, height=10, relief=GROOVE, wrap='word',
                              font=base_font)
    description_widget.insert(1.0,
                              "Welcome to an 80s Style Dialogue Adventure Game Based on the Critically Acclaimed Film Adaptation of Steven Kings 1982 novella, Good Luck!")
    description_widget.config(state="disabled")
    description_widget.grid(row=1, column=0, columnspan=5, sticky="", padx=px(2), pady=px(2))

    controls_frame = ttk.Frame(root)
    controls_frame.grid(row=2, column=0, columnspan=2, padx=px(2), pady=px(2), sticky="w")

    PLACEHOLDER = "What would you like to do?..."

    command_widget = Text(controls_frame, width=19, height=1,
                          bg="#00008b", fg="#aaaaaa", insertbackground="white",
                          font=small_font, relief=GROOVE, bd=2)
    command_widget.insert("1.0", PLACEHOLDER)
    command_widget.bind('<Return>', return_key_enter)
    command_widget.grid(row=0, column=0, padx=(px(2), 0), pady=(px(2), 0), sticky="ew")

    def on_focus_in(event):
        if command_widget.get("1.0", END).strip() == PLACEHOLDER:
            command_widget.delete("1.0", END)
            command_widget.config(fg="white")

    def on_focus_out(event):
        if command_widget.get("1.0", END).strip() == "":
            command_widget.insert("1.0", PLACEHOLDER)
            command_widget.config(fg="#aaaaaa")

    command_widget.bind("<FocusIn>", on_focus_in)
    command_widget.bind("<FocusOut>", on_focus_out)

    button_frame = ttk.Frame(controls_frame)
    button_frame.config(relief=GROOVE)
    button_frame.grid(row=1, column=0, padx=px(2), pady=px(2), sticky="w")

    btn_opts = dict(width=5, height=2, relief=RAISED,
                    bg="#4a90d9", fg="white", activebackground="#2c6fad",
                    activeforeground="white", font=btn_font,
                    cursor="hand2", bd=2)

    north_button = Button(button_frame, text="N", command=north_button_click, **btn_opts)
    north_button.grid(row=0, column=1, padx=px(4), pady=px(4))

    south_button = Button(button_frame, text="S", command=south_button_click, **btn_opts)
    south_button.grid(row=2, column=1, padx=px(4), pady=px(4))

    east_button = Button(button_frame, text="E", command=east_button_click, **btn_opts)
    east_button.grid(row=1, column=2, padx=px(4), pady=px(4))

    west_button = Button(button_frame, text="W", command=west_button_click, **btn_opts)
    west_button.grid(row=1, column=0, padx=px(4), pady=px(4))

    inventory_widget = Text(root, width=20, height=8, relief=GROOVE, state=DISABLED,
                            font=base_font)
    inventory_widget.grid(row=2, column=2, rowspan=2, padx=px(2), pady=px(2), sticky=W)

    # Centre the window once widgets have determined its natural size
    root.update_idletasks()
    w = root.winfo_reqwidth()
    h = root.winfo_reqheight()
    root.geometry(f"+{(screen_w - w) // 2}+{(screen_h - h) // 2}")


def set_current_state():
    global refresh_location
    global refresh_objects_visible

    if refresh_location:
        describe_current_location()
        set_current_image()

    if refresh_location or refresh_objects_visible:
        describe_current_visible_objects()

    handle_special_condition()
    set_directions_to_move()
    if not end_of_game:
        describe_current_inventory()

    refresh_location = False
    refresh_objects_visible = False

    command_widget.config(state=("disabled" if end_of_game else "normal"))


def north_button_click():
    print_to_description("N", True)
    perform_command("N", "")
    set_current_state()


def south_button_click():
    print_to_description("S", True)
    perform_command("S", "")
    set_current_state()


def east_button_click():
    print_to_description("E", True)
    perform_command("E", "")
    set_current_state()


def west_button_click():
    print_to_description("W", True)
    perform_command("W", "")
    set_current_state()


def return_key_enter(event):
    if event.widget == command_widget:
        command_string = command_widget.get("1.0", END).strip()
        if command_string == "" or command_string == "What would you like to do?":
            return "break"
        print_to_description(command_string, True)

        command_widget.delete("1.0", END)
        words = command_string.split(' ', 1)
        verb = words[0]
        noun = words[1] if len(words) > 1 else ""
        perform_command(verb.upper(), noun.upper())

        set_current_state()
    return "break"  # prevents Text widget inserting a newline on Return


def set_directions_to_move():
    move_to_north = get_location_to_north() > 0 and not end_of_game
    move_to_south = get_location_to_south() > 0 and not end_of_game
    move_to_east = get_location_to_east() > 0 and not end_of_game
    move_to_west = get_location_to_west() > 0 and not end_of_game

    for btn, enabled in [(north_button, move_to_north), (south_button, move_to_south),
                         (east_button, move_to_east), (west_button, move_to_west)]:
        if enabled:
            btn.config(state=NORMAL, bg="#4a90d9", fg="white")
        else:
            btn.config(state=DISABLED, bg="#a0a0a0", fg="#d0d0d0")


def main():
    build_interface()
    set_current_state()
    root.mainloop()


main()
import datetime
from colorama import Fore
from dateutil import parser

from infrastructure.switchlang import switch
import infrastructure.state as state
import services.data_service as svc


def run():
    print(' ****************** Welcome host **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', create_account)
            s.case('l', log_into_account)
            s.case('y', list_cages)
            s.case('r', register_cage)
            s.case('u', update_availability)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an [a]ccount')
    print('[L]ogin to your account')
    print('List [y]our cages')
    print('[R]egister a cage')
    print('[U]pdate cage availability')
    print('[V]iew your bookings')
    print('Change [M]ode (guest or host)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def create_account():
    print(' ****************** REGISTER **************** ')

    name = input("What is your name?")
    email = input("What is your email?").strip().lower()



    old_account = svc.find_account_by_email(email)
    if old_account:
        error_msg(f"Error: account with {email} already exists.")

    state.active_account = svc.create_account(name, email)
    success_msg(f"Created new account with id: {state.active_account.id}")


def log_into_account():
    print(' ****************** LOGIN **************** ')
    name = input("What is your name?")
    email = input("What is your email?").strip().lower()

    account = svc.find_account_by_email(email)
    if not account:
        error_msg(f"Could not find account with email {email}")

    state.active_account = account
    success_msg("Logged in successfully")

def register_cage():
    print(' ****************** REGISTER CAGE **************** ')

    if not state.active_account:
        error_msg("You must loggin first to register a cage!")
        return

    meters = input("How many square meters is the cage?")
    if not meters:
        error_msg("Cancel")
        return

    meters = float(meters)
    carpeted = input("Is it carpeted (y/n)").lower().startswith("y")
    has_toys = input("Toys?").lower().startswith("y")
    allow_dangerous = input("Can you host venomous snakes (y/n)?").lower().startswith("y")
    name = input("Give your cage a name: ")

    svc.register_cage(
        state.active_account,
        meters,
        carpeted,
        has_toys,
        allow_dangerous,
        name
    )

    state.reload_account()









def list_cages(suppress_header=False):
    if not suppress_header:
        print(' ******************     Your cages     **************** ')

    if not state.active_account:
        error_msg('You must login first to register a cage.')
        return

    cages = svc.find_cages_for_user(state.active_account)
    print(f"You have {len(cages)} cages.")
    for idx, c in enumerate(cages):
        print(f' {idx + 1}. {c.name} is {c.square_meters} meters.')
        for b in c.bookings:
            print('      * Booking: {}, {} days, booked? {}'.format(
                b.check_in_date,
                (b.check_out_date - b.check_in_date).days,
                'YES' if b.booked_date is not None else 'no'
            ))


def update_availability():
    print(' ****************** Add available date **************** ')


def view_bookings():
    print(' ****************** Your bookings **************** ')




def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)

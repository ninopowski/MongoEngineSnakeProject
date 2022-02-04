from data.cages import Cage
from data.owners import Owner

def create_account(name: str, email: str) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email

    owner.save()

    return owner

def find_account_by_email(email: str) -> Owner:

    owner = Owner.objects().filter(email=email).first()
    return owner


def register_cage(active_account: Owner, meters, carpeted, has_toys, allow_dangerous, name) -> Cage:
    cage = Cage()
    cage.meters = meters
    cage.carpeted = carpeted
    cage.has_toys = has_toys
    cage.allow_dangerous_snakes = allow_dangerous
    cage.name = name

    cage.save()

    account = find_account_by_email(active_account.email)
    account.cage_ids.append(cage.id)
    cage.save()

    return cage
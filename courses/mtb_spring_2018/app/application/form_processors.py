def compile_errors(form):
    errs = []
    for field, errors in form.errors.items():
        for error in errors:
            text = u"Error in the %s field - %s" % (getattr(form, field).label.text, error)
            errs.append(text)
    return errs

def get_current_user_id():
    c_u = github.get('user')
    u_name = str(c_u['login'])
    u = User.query.filter(User.username==u_name).one_or_none()
    return int(u.id)

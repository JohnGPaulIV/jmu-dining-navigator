from app import db
from flask import flash, redirect
from flask_appbuilder import SimpleFormView
from markupsafe import Markup
from flask_appbuilder.forms import DynamicForm
from flask_login import current_user
from wtforms import SelectMultipleField, StringField, SelectField, TextAreaField, widgets
from wtforms.validators import InputRequired, Optional, ValidationError, Length
from models import DietaryRestriction, DiningUser, Ticket


# ========== DIETARY PREFERENCES FORM ==========

class DietaryPreferencesForm(DynamicForm):
    """Form for users to select their dietary restrictions."""
    
    username = StringField(
        "Username",
        validators=[Optional()],
        description="Enter your username (only if not logged in)."
    )
    
    restrictions = SelectMultipleField(
        "Dietary Restrictions",
        coerce=int,
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
        description="Select all that apply."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hide username field if user is logged in
        if current_user.is_authenticated:
            if 'username' in self._fields:
                del self._fields['username']
        else:
            self.username.validators = [InputRequired()]

        self.pre_fill()

    def pre_fill(self):
        """Populate the restrictions dropdown from the database."""
        all_restrictions = db.session.query(DietaryRestriction).order_by(DietaryRestriction.name).all()
        self.restrictions.choices = [
            (r.dietary_restriction_id, r.name) for r in all_restrictions
        ]


class DietaryPreferencesView(SimpleFormView):
    route_base = "/preferences"
    form = DietaryPreferencesForm
    form_title = "Update Dietary Preferences"
    message = "Preferences updated successfully."

    def form_get(self, form):
        """Pre-check boxes based on existing user preferences."""
        target_user = None
        
        if current_user.is_authenticated:
            target_user = db.session.get(DiningUser, current_user.id)
        else:
            # If username field exists, try to find user
            if hasattr(form, 'username') and form.username.data:
                target_user = db.session.query(DiningUser).filter_by(name=form.username.data).first()
        
        if target_user:
            form.restrictions.data = [r.dietary_restriction_id for r in target_user.dietary_restrictions]

    def form_post(self, form):
        """Save the user's dietary restrictions to the database."""
        target_user = self._get_target_user(form)
        
        if target_user:
            # Clear existing restrictions and add new ones
            target_user.dietary_restrictions = []
            for r_id in form.restrictions.data:
                restriction = db.session.get(DietaryRestriction, r_id)
                if restriction:
                    target_user.dietary_restrictions.append(restriction)
            
            db.session.commit()
            flash(self.message, "success")
        else:
            flash("User not found.", "danger")
        
        return redirect(self.get_redirect())

    def _get_target_user(self, form):
        """Helper to find or create the target user."""
        if current_user.is_authenticated:
            user = db.session.get(DiningUser, current_user.id)
            
            if not user:
                # Create new user entry if doesn't exist
                user = DiningUser(
                    user_id=current_user.id,
                    name=current_user.username,
                    email=current_user.email
                )
                db.session.add(user)
                db.session.commit()
            else:
                # Update existing user with current admin info
                user.name = current_user.username
                user.email = current_user.email
            
            return user
        else:
            # Not logged in: find by username field
            name_input = form.username.data
            return db.session.query(DiningUser).filter_by(name=name_input).first()


# ========== HELP & SUPPORT FORM ==========

class HelpForm(DynamicForm):
    """Form for users to submit support tickets."""
    
    username = StringField(
        "Username",
        validators=[Optional()],
        description="Enter your username (only if not logged in)."
    )
    
    details = TextAreaField(
        "Question or Complaint",
        validators=[InputRequired(), Length(max=1000)],
        description="Describe your issue (max 1000 chars)."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hide username field if user is logged in
        if current_user.is_authenticated:
            if 'username' in self._fields:
                del self._fields['username']
        else:
            self.username.validators = [InputRequired()]


class HelpFormView(SimpleFormView):
    route_base = "/support"
    form = HelpForm
    form_title = "Help & Support"
    template = "help_form.jinja"

    def form_post(self, form):
        """Save the support ticket to the database."""
        target_user = self._get_target_user(form)

        if not target_user:
            flash("User profile not found. Please check the username.", "danger")
            return redirect(self.get_redirect())

        ticket = Ticket(
            user_id=target_user.user_id,
            message=form.details.data
        )
        db.session.add(ticket)
        db.session.commit()
        
        flash("Your ticket has been submitted.", "success")
        return redirect(self.get_redirect())

    def _get_target_user(self, form):
        """Helper to find or create the target user."""
        if current_user.is_authenticated:
            user = db.session.get(DiningUser, current_user.id)
            
            if not user:
                # Create new user entry if doesn't exist
                user = DiningUser(
                    user_id=current_user.id,
                    name=current_user.username,
                    email=current_user.email
                )
                db.session.add(user)
                db.session.commit()
            else:
                # Update existing user with current info
                user.name = current_user.username
                user.email = current_user.email
            
            return user
        else:
            # Not logged in, find by username field
            name_input = form.username.data
            return db.session.query(DiningUser).filter_by(name=name_input).first()
from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import URLForm
from app.models import JobResult
from app.tasks import count_words_at_url
from app import rq

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = form.url.data.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        job = rq.get_queue().enqueue(
            count_words_at_url, args=(url,), job_timeout="5m"
        )
        JobResult.create(url, job.id)
        flash("Job submitted successfully!", "success")
        return redirect(url_for("main.index"))

    jobs = JobResult.get_all()
    return render_template("index.html", form=form, jobs=jobs)

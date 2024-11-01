from flask import Blueprint, render_template, flash, redirect, url_for, jsonify, request
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
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"job_id": job.id})
        
        flash("Job submitted successfully!", "success")
        return redirect(url_for("main.index"))
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            "errors": {
                "url": form.url.errors
            }
        }), 400

    jobs = JobResult.get_all()
    return render_template("index.html", form=form, jobs=jobs)


@main.route("/api/jobs/<job_id>", methods=["GET"])
def get_job_status(job_id):
    job = JobResult.get_by_id(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    
    return jsonify({
        "status": job["status"],
        "word_count": job["word_count"],
        "words": job["words"] if "words" in job else [],
        "error": job["error"]
    })

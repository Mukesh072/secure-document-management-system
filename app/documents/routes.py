import os
from flask import (
    Blueprint, render_template, redirect, url_for, flash,
    request, current_app, abort
)
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Document
from app.utils.s3_utils import (
    upload_file_to_s3, delete_file_from_s3,
    generate_presigned_url, generate_s3_key
)

documents_bp = Blueprint("documents", __name__)


def allowed_file(filename):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


@documents_bp.route("/dashboard")
@login_required
def dashboard():
    docs = (
        Document.query.filter_by(user_id=current_user.id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )
    return render_template("dashboard.html", documents=docs)


@documents_bp.route("/upload", methods=["POST"])
@login_required
def upload():
    if "file" not in request.files:
        flash("No file selected.", "danger")
        return redirect(url_for("documents.dashboard"))

    file = request.files["file"]

    if file.filename == "":
        flash("No file selected.", "danger")
        return redirect(url_for("documents.dashboard"))

    if not allowed_file(file.filename):
        flash("File type not allowed.", "danger")
        return redirect(url_for("documents.dashboard"))

    filename = os.path.basename(file.filename)
    s3_key = generate_s3_key(current_user.id, filename)

    # figure out file size without loading whole file into memory twice
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    success = upload_file_to_s3(file, s3_key, content_type=file.content_type)

    if not success:
        flash("Upload failed. Please try again.", "danger")
        return redirect(url_for("documents.dashboard"))

    doc = Document(
        original_filename=filename,
        s3_key=s3_key,
        file_size=file_size,
        content_type=file.content_type,
        user_id=current_user.id,
    )
    db.session.add(doc)
    db.session.commit()

    current_app.logger.info(f"User {current_user.username} uploaded file: {filename}")
    flash("File uploaded successfully.", "success")
    return redirect(url_for("documents.dashboard"))


@documents_bp.route("/download/<int:doc_id>")
@login_required
def download(doc_id):
    doc = Document.query.get_or_404(doc_id)

    if doc.user_id != current_user.id:
        current_app.logger.warning(
            f"Unauthorized download attempt by {current_user.username} on doc {doc_id}"
        )
        abort(403)

    url = generate_presigned_url(
    doc.s3_key,
    doc.original_filename
) 
    print(url)
    
    if not url:
        flash("Could not generate download link.", "danger")
        return redirect(url_for("documents.dashboard"))

    current_app.logger.info(f"User {current_user.username} downloaded file: {doc.original_filename}")
    return redirect(url)


@documents_bp.route("/delete/<int:doc_id>", methods=["POST"])
@login_required
def delete(doc_id):
    doc = Document.query.get_or_404(doc_id)

    if doc.user_id != current_user.id:
        current_app.logger.warning(
            f"Unauthorized delete attempt by {current_user.username} on doc {doc_id}"
        )
        abort(403)

    delete_file_from_s3(doc.s3_key)
    db.session.delete(doc)
    db.session.commit()

    current_app.logger.info(f"User {current_user.username} deleted file: {doc.original_filename}")
    flash("File deleted successfully.", "info")
    return redirect(url_for("documents.dashboard"))

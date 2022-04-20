from flask import (Blueprint, url_for, redirect, render_template,
        request, flash, current_app, send_file, abort)
from flask_login import login_required,current_user
from project.files.forms import LinkForm, AdvancedForm
from project.files.utils import file_details,file_type
from project.models import Folder,User,SubFiles
from project import db
import subprocess,os
from threading import Thread


script_location = os.path.join(os.getcwd(),'project/storage')
print(script_location)

files = Blueprint('files', __name__)

def asyn_run_command(filename, command,user_id,split=None):
    folder = Folder.query.filter_by(name=filename).filter_by(user_id=user_id).first()
    result = subprocess.run(command, shell=True, cwd=script_location, stdout=subprocess.PIPE)
    if result.returncode == 0:
        if split:
            size,location,*subfiles,_ = result.stdout.decode().split('\n')
            folder.size = int(int(size)/1024)
            folder.location = location
            folder.splited = True
            for subfile in subfiles:
                name,size = subfile.split(' :')
                size = int(int(size)/1024)
                location = os.path.join(folder.location,name)
                sub = SubFiles(
                        name = name,
                        size = size,
                        location = location,
                        folder_id = folder.id
                        )
                db.session.add(sub)
            folder.progress = 'Finished'
        else:
            size,location,_ = result.stdout.decode().split('\n')
            folder.size = int(int(size)/1024)
            folder.location = location
            folder.progress = 'Finished'
    elif result.returncode == 2:
        folder.progress = 'Virus'
        folder.virus = True
    elif result.returncode == 1:
        folder.progress = 'Failed'
    db.session.commit()

def run_command(filename, url, location, user_id, split=None, level=9):
    command = f"./download.sh -u '{url}' -l '{location}' -f '{filename}' -c {level}"
    if split:
        command += f' -s {split}'
    print(command)
    Thread(target=asyn_run_command, args=(filename,command,user_id,split)).start()


@files.route('/files', methods=['POST','GET'])
@login_required
def file():
    link_form = LinkForm()
    
    if link_form.validate_on_submit():
        details = file_details(link_form.link.data)
        print(details)

        if not details:
            flash('Cant find downloading link','danger')
            return redirect(url_for('files.file'))

        filename,url,size,content_type = details
        size = int(int(size)/1024)
        if size/1024 > 200:
            flash('Maximum file size is 200','danger')
            return redirect(url_for('files.file'))
        content_type = file_type(content_type)

        folder = Folder.query.filter_by(name=filename).filter_by(user_id=current_user.id).first()
        if folder:
            flash(f'{filename} already exist','danger')
            link_form.link.data=''
            return redirect(url_for('files.file'))
        
        file_location = os.path.join(script_location,current_user.username+f'/{filename}')

        folder = Folder(
                name = filename,
                location = current_user.username,
                size = size,
                content_type = content_type,
                user_id = current_user.id,
                file_location = file_location
                )
        db.session.add(folder)
        db.session.commit()
        run_command(filename=filename,url=url,location=folder.location,user_id=current_user.id)
        link_form.link.data = ''
        flash(f'{details[0]} is successfully added to the list','success')
        return redirect('/files')
    return render_template('files.html', link_form=link_form, files=current_user.files)

@files.route('/show')
def showfolder():
    data = [ str(file) for file in current_user.files]
    print(data)
    return 'fskjfl'

@files.route('/share/<string:token>')
def share_link(token):
    folder = Folder.check_token(token)
    if folder is None:
        abort(404)
    location = os.path.join(script_location, folder.location)
    filename = location.split('/')[-1]
    return send_file(location, as_attachment=True)

@files.route('/get_link/<int:id>')
@login_required
def share(id):
    link_form = LinkForm()
    folder = Folder.query.get(id)
    if not folder:
        return redirect('/files')
    if folder.owner != current_user or folder.progress != 'Finished':
        abort(403)
    token = folder.get_token()
    link = url_for('files.share_link',token=token,_external=True)
    return render_template('link_copy.html',link=link, link_form=link_form)


@files.route('/download/<int:id>')
@login_required
def download(id):
    folder = Folder.query.get(id)
    if not folder:
        return redirect('/files')
    if folder.owner != current_user or folder.progress != 'Finished':
        abort(403)
    location = os.path.join(script_location, folder.location)
    filename = location.split('/')[-1]
    return send_file(location, as_attachment=True)

@files.route('/subfiles/share/<string:token>')
def sub_share_link(token):
    folder = SubFiles.check_token(token)
    if folder is None:
        abort(404)
    location = os.path.join(script_location, folder.location)
    filename = location.split('/')[-1]
    return send_file(location, as_attachment=True)

@files.route('/subfiles/get_link/<int:id>')
@login_required
def sub_share(id):
    link_form = LinkForm()
    folder = SubFiles.query.get(id)
    if not folder:
        return redirect('/files')
    if folder.main.owner != current_user or folder.main.progress != 'Finished':
        abort(403)
    token = folder.get_token()
    link = url_for('files.sub_share_link',token=token,_external=True)
    return render_template('link_copy.html',link=link, link_form=link_form)


@files.route('/subfiles/download/<int:id>')
@login_required
def sub_download(id):
    folder = SubFiles.query.get(id)
    if not folder:
        return redirect('/files')
    if folder.main.owner != current_user or folder.main.progress != 'Finished':
        abort(403)
    location = os.path.join(script_location, folder.location)
    filename = location.split('/')[-1]
    return send_file(location, as_attachment=True)

@files.route('/advanced', methods=["POST", "GET"])
@login_required
def advanced():
    link_form = LinkForm()
    advanced_form = AdvancedForm()
    if advanced_form.validate_on_submit():
        details = file_details(advanced_form.link.data)

        if not details:
            flash('Cant find downloading link','danger')
            return redirect(url_for('files.file'))

        filename,url,size,content_type = details
        size = int(int(size)/1024)
        if size/1024 > 200:
            flash('Maximum file size is 200','danger')
            return redirect(url_for('files.file'))
        content_type = file_type(content_type)

        folder = Folder.query.filter_by(name=filename).filter_by(user_id=current_user.id).first()
        if folder:
            flash(f'{filename} already exist','danger')
            link_form.link.data=''
            return redirect(url_for('files.file'))

        file_location = os.path.join(script_location,current_user.username+f'/{filename}')

        folder = Folder(
                name = filename,
                location = current_user.username,
                size = size,
                content_type = content_type,
                user_id = current_user.id,
                file_location =file_location
                )
        db.session.add(folder)
        db.session.commit()
        level = advanced_form.level.data
        split = advanced_form.split.data 
        if level == 'medium':
            level = 5
        elif level == 'low':
            level = 2
        else:
            level = 9
        split = None if split == "None" else split
        run_command(filename=filename,url=url,location=folder.location, user_id=current_user.id, level=level, split=split)
        link_form.link.data = ''
        advanced_form.link.data = ''
        flash(f'{details[0]} is successfully added to the list','success')
        return redirect('/files')
    return render_template('advanced.html', link_form=link_form, advanced_form=advanced_form)

@files.route('/files/subfiles/<int:folder_id>')
@login_required
def subfiles(folder_id):
    link_form = LinkForm()
    folder = Folder.query.get(folder_id)
    #return f'{folder.name}'
    if folder is None or not folder.splited:
        abort(404)
    if folder.owner != current_user:
        abort(403)
    return render_template('subfiles.html', files=folder.subfiles, link_form=link_form) 

@files.route('/files/view/<int:id>')
@login_required
def view_files(id):
    link_form = LinkForm()
    file = Folder.query.get(id)
    if not file:
        abort(404)
    if file.owner != current_user:
        abort(403)
    if 'video' in file.content_type:
        return render_template('video.html', link_form=link_form,id=file.id)
    elif 'pdf' in file.content_type:
        return render_template('pdfviewer.html', link_form=link_form,id=file.id)
    else:
        abort(404)

@files.route('/files/video/<int:id>')
@login_required
def view_video(id):
    file = Folder.query.get(id)
    if not file:
        abort(404)
    if file.owner != current_user:
        abort(403)
    if 'video' in file.content_type:
        print('\n entered\n')
        location = os.path.join(script_location, file.file_location)
        return send_file(location)

@files.route('/files/pdf/<int:id>')
@login_required
def view_pdf(id):
    file = Folder.query.get(id)
    if not file:
        abort(404)
    if file.owner != current_user:
        abort(403)
    if 'pdf' in file.content_type:
        location = os.path.join(script_location, file.file_location)
        return send_file(location)

def clean_up(locations):
    for location in locations:
        command = f"rm -rf '{location}'"
        subprocess.run(command, shell=True)

@files.route('/files/delete/<int:id>')
@login_required
def delete(id):
    file = Folder.query.get(id)
    if not file:
        abort(404)
    if file.owner != current_user:
        abort(403)
    if file.progress == 'Processing':
        abort(404)
    if file.virus:
        locations = [file.file_location]
    else:
        locations = [ file.file_location, os.path.join(script_location,file.location) ]
    if file.splited:
        for f in file.subfiles:
            db.session.delete(f)
    Thread(target=clean_up, args=(locations,)).start()
    db.session.delete(file)
    db.session.commit()
    return redirect(url_for('files.file'))

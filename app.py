from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clave para las sesiones

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Servidor SMTP (ej. Gmail)
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu_correo@gmail.com'  # Cambia por tu correo
app.config['MAIL_PASSWORD'] = 'tu_contraseña'  # Cambia por tu contraseña
app.config['MAIL_DEFAULT_SENDER'] = 'tu_correo@gmail.com'  # Remitente por defecto

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proyectos')
def proyectos():
    return render_template('proyectos.html')

@app.route('/sobre-mi')
def sobre_mi():
    return render_template('sobre_mi.html')

@app.route('/curriculum3D')
def curriculum3D():
    return render_template('curriculum3D.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Crear el mensaje
        msg = Message(subject=f"Mensaje de {name}",
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=['tu_destinatario@gmail.com'])  # Correo donde recibirás los mensajes
        msg.body = f"De: {name} <{email}>\n\nMensaje:\n{message}"

        try:
            mail.send(msg)
            flash('¡Tu mensaje ha sido enviado correctamente!', 'success')
        except Exception as e:
            flash(f'Error al enviar el mensaje: {e}', 'error')
        
        return redirect(url_for('contacto'))

if __name__ == '__main__':
    app.run(debug=True)

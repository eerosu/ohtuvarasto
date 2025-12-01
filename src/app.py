from flask import Flask, render_template, request, redirect, url_for, flash, session
from varasto import Varasto
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store warehouses in session (in production, this would be a database)
def get_warehouses():
    if 'warehouses' not in session:
        session['warehouses'] = []
    return session['warehouses']

def save_warehouses(warehouses):
    session['warehouses'] = warehouses

@app.route('/')
def index():
    warehouses = get_warehouses()
    return render_template('index.html', warehouses=warehouses)

@app.route('/new', methods=['GET', 'POST'])
def new_warehouse():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        try:
            tilavuus = float(request.form.get('tilavuus', 0))
            alku_saldo = float(request.form.get('alku_saldo', 0))
            
            if not name:
                flash('Nimi on pakollinen', 'error')
                return render_template('new.html')
            
            if tilavuus <= 0:
                flash('Tilavuuden on oltava suurempi kuin 0', 'error')
                return render_template('new.html')
            
            varasto = Varasto(tilavuus, alku_saldo)
            warehouses = get_warehouses()
            warehouses.append({
                'id': len(warehouses),
                'name': name,
                'tilavuus': varasto.tilavuus,
                'saldo': varasto.saldo
            })
            save_warehouses(warehouses)
            flash('Varasto luotu onnistuneesti', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Virheelliset arvot', 'error')
            return render_template('new.html')
    
    return render_template('new.html')

@app.route('/edit/<int:warehouse_id>', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    warehouses = get_warehouses()
    if warehouse_id >= len(warehouses) or warehouse_id < 0:
        flash('Varastoa ei löytynyt', 'error')
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        try:
            tilavuus = float(request.form.get('tilavuus', 0))
            
            if not name:
                flash('Nimi on pakollinen', 'error')
                return render_template('edit.html', warehouse=warehouse)
            
            if tilavuus <= 0:
                flash('Tilavuuden on oltava suurempi kuin 0', 'error')
                return render_template('edit.html', warehouse=warehouse)
            
            # Make sure saldo doesn't exceed new tilavuus
            if warehouse['saldo'] > tilavuus:
                warehouse['saldo'] = tilavuus
            
            warehouse['name'] = name
            warehouse['tilavuus'] = tilavuus
            warehouses[warehouse_id] = warehouse
            save_warehouses(warehouses)
            flash('Varasto päivitetty onnistuneesti', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Virheelliset arvot', 'error')
            return render_template('edit.html', warehouse=warehouse)
    
    return render_template('edit.html', warehouse=warehouse)

@app.route('/add/<int:warehouse_id>', methods=['GET', 'POST'])
def add_to_warehouse(warehouse_id):
    warehouses = get_warehouses()
    if warehouse_id >= len(warehouses) or warehouse_id < 0:
        flash('Varastoa ei löytynyt', 'error')
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    
    if request.method == 'POST':
        try:
            maara = float(request.form.get('maara', 0))
            
            varasto = Varasto(warehouse['tilavuus'], warehouse['saldo'])
            varasto.lisaa_varastoon(maara)
            
            warehouse['saldo'] = varasto.saldo
            warehouses[warehouse_id] = warehouse
            save_warehouses(warehouses)
            flash(f'Lisättiin {maara} varastoon', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Virheellinen määrä', 'error')
            return render_template('add.html', warehouse=warehouse)
    
    return render_template('add.html', warehouse=warehouse)

@app.route('/remove/<int:warehouse_id>', methods=['GET', 'POST'])
def remove_from_warehouse(warehouse_id):
    warehouses = get_warehouses()
    if warehouse_id >= len(warehouses) or warehouse_id < 0:
        flash('Varastoa ei löytynyt', 'error')
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    
    if request.method == 'POST':
        try:
            maara = float(request.form.get('maara', 0))
            
            varasto = Varasto(warehouse['tilavuus'], warehouse['saldo'])
            saatu = varasto.ota_varastosta(maara)
            
            warehouse['saldo'] = varasto.saldo
            warehouses[warehouse_id] = warehouse
            save_warehouses(warehouses)
            flash(f'Otettiin {saatu} varastosta', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Virheellinen määrä', 'error')
            return render_template('remove.html', warehouse=warehouse)
    
    return render_template('remove.html', warehouse=warehouse)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

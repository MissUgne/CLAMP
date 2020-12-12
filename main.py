#     <CLAMP CALCULATOR. Web based application for a CLAMP data calculation>
#     Copyright (C) 2020  Ugne Gliaudelyte
#
#     CLAMP CALCULATOR is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     CLAMP CALCULATOR is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with CLAMP CALCULATOR.  If not, see <https://www.gnu.org/licenses/>.
#

from flask import Flask, render_template, redirect, request, url_for
import os
from csv import DictWriter

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

flora = {
    'no': 'None',
    'bh': 'Blackhawk Formation',
    'mc': 'Mazon Creek',
    'cf': 'Clairebone Formation',
}

specimen = {
    'no': 'None',
    'sp1': 'Spiropteris sp.',
    'sp2': 'Crenulopteris acadica',
    'sp3': 'Radstockia kidstonii',
}

@app.route('/taxonomy', methods=['GET', 'POST'])
def taxonomy():
    if request.method == 'POST':
        numb = request.form['fmhn']
        result.update({'FMHN No': numb})
        print(numb)
        return redirect(url_for('lobing', scores=scores))
    return render_template('taxonomy.html', specimen=specimen, flora=flora)


scores = {
    'sc0': 0,
    'sc025': 0.25,
    'sc033': 0.33,
    'sc05': 0.5,
    'sc1': 1,
}


result = {

}

# 1. Lobing: 6 photos
# 0 if no leaves are lobed; 1 if all leaves lobed
@app.route('/lobing', methods=['GET', 'POST'])
def lobing():
    if request.method == 'POST':
        lobe = request.form['scores']
        result.update({'Lobing': lobe})
        return redirect(url_for('margin', scores=scores))
    return render_template('lobing.html', scores=scores)


# 2. Leaf margin: 7 different shapes (if one of first three selected, moves to 3)
@app.route('/margin', methods=['GET', 'POST'])
def margin():
    if request.method == 'POST':
        final_margin = request.form['scores']
        if final_margin == '0' or final_margin == '0.5':
            result.update({'Margin': final_margin})
            return redirect(url_for('regular', scores=scores))
        else:
            result.update({'Margin': 1})
            result.update({'Regularity': 0})
            result.update({'Closeness': 0})
            result.update({'Teethshape': 0})
            result.update({'Acute': 0})
            result.update({'Compound': 0})
            return redirect(url_for('apex', scores=scores))
    return render_template('margin.html', scores=scores)


#   2.1 Regularity of teeth: 4 photos
@app.route('/regular', methods=['GET', 'POST'])
def regular():
    if request.method == 'POST':
        final_regular = request.form['scores']
        result.update({'Regularity': final_regular})
        return redirect(url_for('close', scores=scores))
    return render_template('regular.html', scores=scores)


#   2.2. Closeness of teeth: 4 photos
@app.route('/close', methods=['GET', 'POST'])
def close():
    if request.method == 'POST':
        final_close = request.form['scores']
        result.update({'Closeness': final_close})
        return redirect(url_for('teethshape', scores=scores))
    return render_template('close.html', scores=scores)


#   2.3. Teeth rounded and (or) appressed: 4 photos
@app.route('/teethshape', methods=['GET', 'POST'])
def teethshape():
    if request.method == 'POST':
        final_teethshape = request.form['scores']
        result.update({'Teethshape': final_teethshape})
        return redirect(url_for('acute', scores=scores))
    return render_template('teethshape.html', scores=scores)


#   2.4 Acute: 2 photos
@app.route('/acute', methods=['GET', 'POST'])
def acute():
    if request.method == 'POST':
        final_acute = request.form['scores']
        result.update({'Acute': final_acute})
        return redirect(url_for('compound', scores=scores))
    return render_template('acute.html', scores=scores)


#   2.5. Teeth compound: 2 photos
@app.route('/compound', methods=['GET', 'POST'])
def compound():
    if request.method == 'POST':
        final_compound = request.form['scores']
        print('Compound score: ' + final_compound)
        result.update({'Compound': final_compound})
        return redirect(url_for('apex', scores=scores))
    return render_template('compound.html', scores=scores)


# 3. Apex Form: 16 photos
@app.route('/apex', methods=['GET', 'POST'])
def apex():
    if request.method == 'POST':
        apex1 = int(request.form['group1'])
        apex2 = int(request.form['group2'])
        apex3 = int(request.form['group3'])
        apex4 = int(request.form['group4'])
        totalapex = apex1 + apex2 + apex3 + apex4
        print('Total apex score: ' + str(totalapex))
        if totalapex == 1:
            finalapex = 1
            print('Apex score: ' + str(finalapex))
            result.update({'Apex': finalapex})
        elif 1 < totalapex < 3:
            finalapex = 0.5
            print('Apex score: ' + str(finalapex))
            result.update({'Apex': finalapex})
        elif totalapex == 4:
            finalapex = 0.33
            print('Apex score: ' + str(finalapex))
            result.update({'Apex': finalapex})
        elif totalapex == 0:
            finalapex = 0
            print('Apex score: ' + str(finalapex))
            result.update({'Apex': finalapex})
        return redirect(url_for('base', scores=scores))
    return render_template('apex.html', scores=scores)


# 4. Base Form: 12 photos
@app.route('/base', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        base1 = int(request.form['group1'])
        base2 = int(request.form['group2'])
        base3 = int(request.form['group3'])
        totalbase = base1 + base2 + base3
        print('Total base score: ' + str(totalbase))
        if totalbase == 1:
            finalbase = 1
            result.update({'Base': finalbase})
        elif 1 < totalbase < 3:
            finalbase = 0.5
            result.update({'Base': finalbase})
        elif totalbase == 3:
            finalbase = 0.33
            result.update({'Base': finalbase})
        elif totalbase == 0:
            finalbase = 0
            result.update({'Base': finalbase})
        return redirect(url_for('shape', scores=scores))
    return render_template('base.html', scores=scores)


# 5. Shape: 11 photos
@app.route('/shape', methods=['GET', 'POST'])
def shape():
    if request.method == 'POST':
        shape1 = int(request.form['group1'])
        shape2 = int(request.form['group2'])
        shape3 = int(request.form['group3'])
        totalshape = shape1 + shape2 + shape3
        if totalshape == 1:
            finalshape = 1
            result.update({'Shape': finalshape})
        elif 1 < totalshape < 3:
            finalshape = 0.5
            result.update({'Shape': finalshape})
        elif totalshape == 3:
            finalshape = 0.33
            result.update({'Shape': finalshape})
        elif totalshape == 0:
            finalshape = 0
            result.update({'Shape': finalshape})
        return redirect(url_for('ratio', scores=scores))
    return render_template('shape.html', scores=scores)


# 6. Length-to-width ratio
@app.route('/ratio', methods=['GET', 'POST'])
def ratio():
    global  testratio, testratio2, testratio3
    if request.method == 'POST':
        finalratio = []
        length = int(request.form['length'])
        width = int(request.form['width'])
        ratio = int(length / width)
        length2 = int(request.form['length2'])
        width2 = int(request.form['width2'])
        ratio2 = int(length2 / width2)
        length3 = int(request.form['length3'])
        width3 = int(request.form['width3'])
        ratio3 = int(length3 / width3)

        if 0 < ratio < 1:
            ratio = 1
        elif 1 < ratio < 2:
            ratio = 2
        elif 2 < ratio < 3:
            ratio = 3
        elif 3 < ratio < 4:
            ratio = 4
        elif 4 < ratio:
            ratio = 5
        finalratio.append(ratio)

        if 0 < ratio2 < 1:
            ratio2 = 1
        elif 1 < ratio2 < 2:
            ratio2 = 2
        elif 2 < ratio2 < 3:
            ratio2 = 3
        elif 3 < ratio2 < 4:
            ratio2 = 4
        elif 4 < ratio2:
            ratio2 = 5
        finalratio.append(ratio2)

        if 0 < ratio3 < 1:
            ratio3 = 1
        elif 1 < ratio2 < 2:
            ratio3 = 2
        elif 2 < ratio3 < 3:
            ratio3 = 3
        elif 3 < ratio3 < 4:
            ratio3 = 4
        elif 4 < ratio3:
            ratio3 = 5
        finalratio.append(ratio3)

        if finalratio[2] == finalratio[0] and finalratio[2] == finalratio[1]:
            answer = 1
            result.update({'Ratio': answer})
        elif finalratio[2] == finalratio[0] and finalratio[2] != finalratio[1]:
            answer = 0.5
            result.update({'Ratio': answer})
        elif finalratio[2] == finalratio[1] and finalratio[2] != finalratio[0]:
            answer = 0.5
            result.update({'Ratio': answer})
        elif finalratio[2] != finalratio[1] and finalratio[2] != finalratio[0] and finalratio[0] != finalratio[1]:
            answer = 0.33
            result.update({'Ratio': answer})
        elif finalratio[2] != finalratio[1] and finalratio[2] != finalratio[0] and finalratio[0] == finalratio[1]:
            answer = 0.5
            result.update({'Ratio': answer})
        return redirect(url_for('size', scores=scores))
    return render_template('ratio.html')


# 7. Leaf size
@app.route('/size', methods=['GET', 'POST'])
def size():
    if request.method == 'POST':
        size = len(request.form.getlist('hello'))

        if size == 1:
            finalsize = 1
            result.update({'Size': finalsize})
        elif size == 2:
            finalsize = 0.5
            result.update({'Size': finalsize})
        elif size == 3:
            finalsize = 0.33
            result.update({'Size': finalsize})
        elif size == 4:
            finalsize = 0.25
            result.update({'Size': finalsize})
        elif size == 5:
            finalsize = 0.2
            result.update({'Size': finalsize})
        elif size == 6:
            finalsize = 0.17
            result.update({'Size': finalsize})
        elif size == 7:
            finalsize = 0.14
            result.update({'Size': finalsize})
        elif size == 8:
            finalsize = 0.13
            result.update({'Size': finalsize})
        elif size == 9:
            finalsize = 0.12
            result.update({'Size': finalsize})
        return redirect(url_for('final', scores=scores))
    return render_template('size.html', scores=scores)


@app.route('/final', methods=['GET', 'POST'])
def final():
    if request.method == 'POST':
        df4 = result
    return render_template('final.html', result=result)


file_name = 'scores.csv'
file_exists = os.path.isfile(file_name)

@app.route('/csv', methods=['GET', 'POST'])
def csv():
    def append_dict_as_row(file_name, dict_of_elem, field_names):
        with open(file_name, 'a', newline='') as write_obj:
            # Create a writer object from csv module
            dict_writer = DictWriter(write_obj, fieldnames=field_names)
            # Add header only once
            file_is_empty = os.stat(file_name).st_size == 0
            if file_is_empty:
                dict_writer.writeheader()
            # Add dictionary as a row
            dict_writer.writerow(dict_of_elem)

    # ! ADD IRN FROM DATABASE
    def main():
        field_names = ['IRN', 'FMHN No', 'Lobing', 'Margin', 'Regularity', 'Closeness', 'Teethshape', 'Acute', 'Compound', 'Apex', 'Base',
                       'Shape', 'Ratio', 'Size']
        row_dict = result
        # Append a dict as a row in csv file
        append_dict_as_row(file_name, row_dict, field_names)
        print('Data added to file')

    if __name__ == '__main__':
        main()

    return render_template('csv.html', result=result)


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html')


@app.errorhandler(404)
def internal_error(error):
    return render_template('error.html')


@app.errorhandler(400)
def internal_error(error):
    return render_template('error.html')


if __name__ == '__main__':
    app.run()

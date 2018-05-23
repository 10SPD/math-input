import os
import re
import sys
import symbol_map

color = '#3B3E40'

header = '''/**
 * An autogenerated component that renders the %s iconograpy in SVG.
 *
 * Generated with: https://gist.github.com/crm416/3c7abc88e520eaed72347af240b32590.
 */
const React = require('react'); const PropTypes = require('prop-types');
'''

# A simple template with no PropTypes, for the case in which there are no
# colors in the component.
simple_template = header + '''
const %s = () => {
    return %s;
};

module.exports = %s;
'''
complex_template = header + '''
const %s = React.createClass({
    propTypes: {
        color: PropTypes.string.isRequired,
    },

    render() {
        return %s;
    },
});

module.exports = %s;
'''

index_template = '''/**
 * A directory of autogenerated icon components.
 */

module.exports = {
%s
};
'''

if __name__ == '__main__':
    input_dir_name = sys.argv[1]
    output_dir_name = sys.argv[2]

    filename_map = {}

    for filename in os.listdir(input_dir_name):
        use_simple = True

        svg_filename = filename.split('/')[-1].split('.')[0]

        prefix = 'math-keypad-icon-'
        if svg_filename[:len(prefix)] == prefix:
            svg_filename = svg_filename[len(prefix):]
        else:
            continue

        try:
            symbol_name = symbol_map.filename_to_symbol[svg_filename]
        except:
            print 'Skipping: ' + svg_filename
            continue

        component_name = symbol_name.title().replace('_', '')
        js_filename = symbol_name.lower().replace('_', '-')

        with open(input_dir_name + '/' + filename, 'r') as f:
            contents = f.read()

            # Strip out the namespace tag
            namespace = 'xmlns="http://www.w3.org/2000/svg"'
            namespace_index = contents.index(namespace)
            contents = contents[:namespace_index - 1] + contents[namespace_index + len(namespace):]

            # Replace any colors
            before = contents
            contents = re.sub('"' + color + '"', '{this.props.color}', contents)
            if before != contents:
                use_simple = False

            # Replace the xlink:href tag (special case)
            contents = contents.replace('xlink:href', 'xlinkHref')
            # Replace any other tags
            tags = re.findall(r' (\S+)=', contents)
            for tag in tags:
                pieces = tag.split('-')
                jsx_version = pieces[0] + ''.join(map(lambda x: x.title(), pieces[1:]))
                contents = contents.replace(tag, jsx_version)

        with open(output_dir_name + '/' + js_filename + '.js', 'w') as f:
            template = simple_template if use_simple else complex_template
            f.write(template % (symbol_name, component_name, contents, component_name))

        filename_map[symbol_name] = js_filename

    index_contents = ''
    for symbol_name in filename_map:
        if index_contents:
            index_contents += '\n'
        index_contents += '    %s: require(\'./%s\'),' % (symbol_name, filename_map[symbol_name])

    with open(output_dir_name + '/index.js', 'w') as f:
        f.write(index_template % index_contents)

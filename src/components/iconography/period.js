/**
 * An autogenerated component that renders the PERIOD iconograpy in SVG.
 *
 * Generated with: https://gist.github.com/crm416/3c7abc88e520eaed72347af240b32590.
 */
const React = require('react'); const PropTypes = require('prop-types');

class Period extends React.Component {
    static propTypes = {
        color: PropTypes.string.isRequired,
    };

    render() {
        return <svg width="48" height="48" viewBox="0 0 48 48"><g fill="none" fillRule="evenodd"><path fill="none" d="M0 0h48v48H0z"/><circle fill={this.props.color} cx="24" cy="30" r="2"/></g></svg>;
    }
}

module.exports = Period;

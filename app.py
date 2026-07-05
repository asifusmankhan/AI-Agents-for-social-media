@app.route('/test')
def test():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return jsonify({"key_found": True, "starts_with": key[:10]})
    else:
        return jsonify({"key_found": False})

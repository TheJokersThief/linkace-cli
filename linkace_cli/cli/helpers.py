import tempfile
import os
import toml
from subprocess import call

shared_ctx = {}

EDITOR = os.environ.get('EDITOR', 'vim')
ABS_DIR = os.path.dirname(os.path.abspath(__file__))


def interactive_editor(template_filename: str = None, prefill_data: dict = None):
    """
    Uses the environment's defined editor to interactive edit the details of an object
    such as a link. On save, it returns the contents of the file.
    """
    with open(f'{ABS_DIR}/templates/{template_filename}') as file:
        template = file.read()

    if prefill_data:
        # Load data, merge with template dict and dump with comments again
        template_data = toml.loads(
            template, decoder=toml.decoder.TomlPreserveCommentDecoder()
        )

        for key, val in prefill_data.items():
            if val and key in template_data:
                if isinstance(template_data[key], toml.decoder.CommentValue):
                    template_data[key].val = val
                else:
                    template_data[key] = val

        template = toml.dumps(template_data, encoder=toml.encoder.TomlPreserveCommentEncoder())

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        if template_filename:
            # Populate file with template contents
            tf.write(bytes(template, 'utf-8'))

        tf.flush()
        call([EDITOR, '+set backupcopy=yes', tf.name])
        tf.seek(0)

        data = tf.read()
        return data.decode('utf-8')

package net.endlos.xdt99.xga99;

import com.intellij.formatting.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.TokenType;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.formatter.common.AbstractBlock;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xga99.psi.Xga99Types;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xga99Block extends AbstractBlock {
    private final static TokenSet statements = TokenSet.create(Xga99Types.INSTRUCTION, Xga99Types.DIRECTIVE,
            Xga99Types.PREPROCESSOR, Xga99Types.UNKNOWN_MNEM);
//    private final static TokenSet operators = TokenSet.create(Xga99Types.OP_PLUS, Xga99Types.OP_MINUS,
//            Xga99Types.OP_AST, Xga99Types.OP_MISC);

    private final ASTNode myPreviousNode;
    private final Xga99CodeStyleSettings mySettings;

    public Xga99Block(@NotNull ASTNode node, CodeStyleSettings settings) {
        super(node, null, null);
        myPreviousNode = null;
        mySettings = settings.getCustomSettings(Xga99CodeStyleSettings.class);
    }

    protected Xga99Block(@NotNull ASTNode node, @Nullable ASTNode prevNode, Xga99CodeStyleSettings settings) {
        super(node, null, null);
        myPreviousNode = prevNode;
        mySettings = settings;
    }

    @Override
    protected List<Block> buildChildren() {
        List<Block> blocks = new ArrayList<Block>();
        ASTNode child = myNode.getFirstChildNode();
        ASTNode previousChild = null;
        while (child != null) {
            if (child.getElementType() == Xga99Types.CRLF) {
                previousChild = null;
            } else if (child.getElementType() != TokenType.WHITE_SPACE) {
                if (child.getTextLength() > 0)  // mostly required for potentially empty PsiErrorElement nodes
                    blocks.add(new Xga99Block(child, previousChild, mySettings));
                previousChild = child;
            }
            child = child.getTreeNext();
        }
        return blocks;
    }

    @Override
    public Indent getIndent() {
        IElementType t = this.getNode().getElementType();
        if (statements.contains(t) || t == Xga99Types.COMMENT) {
            return Indent.getNormalIndent();
        }
        return Indent.getNoneIndent();
    }

    @Nullable
    @Override
    public Spacing getSpacing(@Nullable Block child1, @NotNull Block child2) {
        if (child1 instanceof Xga99Block && child2 instanceof Xga99Block) {
            ASTNode left = ((Xga99Block) child1).getNode();
            ASTNode right = ((Xga99Block) child2).getNode();
            // label <-> mnemonic
            if (left.getElementType() == Xga99Types.LABELDEF && statements.contains(right.getElementType())) {
                return pad(mySettings.XGA99_MNEMONIC_TAB_STOP - 1, left.getTextLength());
            }
            // mnemonic <-> operands
            else if (statements.contains(this.getNode().getElementType()) &&
                    ((Xga99Block) child1).myPreviousNode == null) {
                return pad(mySettings.XGA99_OPERANDS_TAB_STOP - mySettings.XGA99_MNEMONIC_TAB_STOP,
                        left.getTextLength());
            }
            // * <-> comments
            // TODO: Needs to be applied twice if separator spacing changed
            else if (right.getElementType() == Xga99Types.COMMENT &&
                    ((Xga99Block) child2).myPreviousNode != null) {
                return pad(mySettings.XGA99_COMMENT_TAB_STOP - mySettings.XGA99_MNEMONIC_TAB_STOP,
                        left.getTextLength());
            }
            // separator <-> argument
            else if (left.getElementType() == Xga99Types.OP_SEP) {
                return fix(mySettings.XGA99_RELAXED ? 1 : 0);
            }
            // argument <-> separator
            else if (right.getElementType() == Xga99Types.OP_SEP) {
                return fix(0);
            }
            // operator <-> operand and vice versa
            /* NOTE: disabled, since we cannot tell A+B from @A+B, -1 from A-1 for now
            else if (operators.contains(left.getElementType()) && right.getElementType() != Xga99Types.OP_REGISTER ||
                    operators.contains(right.getElementType()) && left.getElementType() != Xga99Types.OP_REGISTER) {
                return fix(mySettings.Xga99_RELAXED ? 1 : 0);
            }
            */
        }
        return null;
    }

    @Override
    public boolean isLeaf() {
        return myNode.getFirstChildNode() == null;
    }

    private Spacing pad(int size, int used) {
        if (used < size)
            return Spacing.createSpacing(size - used, size - used, 0, true, 0);
        else
            return null;
    }

    private Spacing fix(int size) {
        return Spacing.createSpacing(size, size, 0, true, 0);
    }
}

// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99r.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xga99r.psi.Xga99RTypes.*;
import net.endlos.xdt99.xga99r.psi.*;
import com.intellij.navigation.ItemPresentation;

public class Xga99RLabeldefImpl extends Xga99RNamedElementImpl implements Xga99RLabeldef {

  public Xga99RLabeldefImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xga99RVisitor visitor) {
    visitor.visitLabeldef(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xga99RVisitor) accept((Xga99RVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  public String getName() {
    return Xga99RPsiImplUtil.getName(this);
  }

  @Override
  public PsiElement setName(String newName) {
    return Xga99RPsiImplUtil.setName(this, newName);
  }

  @Override
  public PsiElement getNameIdentifier() {
    return Xga99RPsiImplUtil.getNameIdentifier(this);
  }

  @Override
  public ItemPresentation getPresentation() {
    return Xga99RPsiImplUtil.getPresentation(this);
  }

}

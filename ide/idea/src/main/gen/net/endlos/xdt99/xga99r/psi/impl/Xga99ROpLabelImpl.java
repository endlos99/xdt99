// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99r.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xga99r.psi.Xga99RTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xga99r.psi.*;
import com.intellij.psi.PsiReference;

public class Xga99ROpLabelImpl extends ASTWrapperPsiElement implements Xga99ROpLabel {

  public Xga99ROpLabelImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xga99RVisitor visitor) {
    visitor.visitOpLabel(this);
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
  public PsiReference getReference() {
    return Xga99RPsiImplUtil.getReference(this);
  }

}